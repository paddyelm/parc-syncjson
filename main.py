from utils.logger import init_logger
from utils.config import load_config
from parsers.psarc_parser import PsarcExtractor
from generators.sync_generator import SyncGenerator
from pathlib import Path
import sys

def main():
    """
    Main function to coordinate the extraction of song XML from PSARC files
    and generation of corresponding sync.json files.

    Loads configuration settings, initializes logging, processes each PSARC
    file in the input folder, and saves the generated sync.json in the output folder.

    Returns:
        None
    """
    config = load_config()
    logger = init_logger(config)

    logger.info("Starting sync.json generation process...")

    input_folder = Path(config['input_folder'])
    output_folder = Path(config['output_folder'])

    if not input_folder.exists():
        logger.error(f"Input folder does not exist: {input_folder}")
        sys.exit(1)

    output_folder.mkdir(parents=True, exist_ok=True)

    for psarc_file in input_folder.glob("*.psarc"):
        logger.info(f"Processing {psarc_file.name}")

        try:
            extractor = PsarcExtractor(psarc_file)
            song_xml = extractor.extract_song_xml()

            if song_xml:
                generator = SyncGenerator(song_xml)
                sync_data = generator.generate_sync()

                output_file = output_folder / f"{psarc_file.stem}_sync.json"
                generator.save_sync(sync_data, output_file)
                logger.info(f"sync.json created: {output_file}")
            else:
                logger.warning(f"No song XML found in {psarc_file.name}")

        except Exception as e:
            logger.exception(f"Error processing {psarc_file.name}: {e}")

    logger.info("All done!")

if __name__ == "__main__":
    main()