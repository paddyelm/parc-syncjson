import struct
import zlib
from pathlib import Path
from typing import Optional
import tempfile

class PsarcExtractor:
    """
    Class to extract files from a PSARC archive.
    """

    def __init__(self, psarc_path: Path):
        """
        Initialize PsarcExtractor.

        Args:
            psarc_path (Path): Path to the .psarc archive file.
        """
        self.psarc_path = psarc_path
        self.temp_dir = Path(tempfile.mkdtemp(prefix='psarc_extract_'))
        self.zlib_block_size = None
        self.num_entries = None
        self.toc_entry_size = None

    def extract_song_xml(self) -> Optional[str]:
        """
        Orchestrates extraction of files and locates the song XML.

        Returns:
            Optional[str]: Path to the extracted song XML file, or None if not found.
        """
        with open(self.psarc_path, 'rb') as f:
            self._read_header(f)
            entries = self._read_toc(f)
            blocks = self._read_blocks(f)
            self._reconstruct_files(entries, blocks)

        for file in self.temp_dir.iterdir():
            if file.name.endswith("song.xml") or "song" in file.name.lower():
                return str(file)

        return None

    def _read_header(self, f):
        """
        Reads and validates the PSARC file header.

        Args:
            f (file object): Opened PSARC file in binary mode.

        Raises:
            ValueError: If the file does not start with 'PSAR' magic bytes.
        """
        magic = f.read(4)
        if magic != b'PSAR':
            raise ValueError("Invalid PSARC file")

        version = struct.unpack(">I", f.read(4))[0]
        self.zlib_block_size = struct.unpack(">I", f.read(4))[0]
        toc_length = struct.unpack(">I", f.read(4))[0]
        self.toc_entry_size = struct.unpack(">I", f.read(4))[0]
        self.num_entries = struct.unpack(">I", f.read(4))[0]

        self._compressed_toc = f.read(toc_length)

    def _read_toc(self, f):
        """
        Decompresses and parses the Table of Contents.

        Args:
            f (file object): Opened PSARC file (positioned after header and TOC).

        Returns:
            List[Tuple[int, int, int]]: List of entries containing file_size, block_index, and length.
        """
        toc_data = zlib.decompress(self._compressed_toc)
        entries = []

        for i in range(self.num_entries):
            entry = toc_data[i * self.toc_entry_size: (i + 1) * self.toc_entry_size]
            md5 = entry[:16]
            file_size = struct.unpack(">I", entry[16:20])[0]
            block_index = struct.unpack(">I", entry[20:24])[0]
            length = struct.unpack(">I", entry[24:28])[0]
            entries.append((file_size, block_index, length))

        return entries

    def _read_blocks(self, f):
        """
        Reads all compressed data blocks from the PSARC.

        Args:
            f (file object): Opened PSARC file positioned at block section.

        Returns:
            List[bytes]: List of decompressed block data chunks.
        """
        blocks = []
        while True:
            block_size_data = f.read(4)
            if not block_size_data:
                break
            block_size = struct.unpack(">I", block_size_data)[0]
            if block_size == 0:
                continue
            block_data = f.read(block_size)
            blocks.append(block_data)
        return blocks

    def _reconstruct_files(self, entries, blocks):
        """
        Reconstructs and writes extracted files based on TOC entries.

        Args:
            entries (List[Tuple[int, int, int]]): List of file metadata.
            blocks (List[bytes]): List of block data.

        Returns:
            None
        """
        for idx, (file_size, block_index, length) in enumerate(entries):
            if length == 0:
                continue
            data = b''.join(blocks[block_index:block_index + (length + self.zlib_block_size - 1) // self.zlib_block_size])
            output_file_path = self.temp_dir / f"extracted_{idx}.bin"
            output_file_path.write_bytes(data[:file_size])
