# Rocksmith PSARC Sync Extractor 🎸

A Python-based tool to extract beatmaps (`sync.json`) and other metadata from Rocksmith `.psarc` song archives.

Designed to be clean, extensible, and highly configurable via YAML settings and modular Python code.

---

## ✨ Features

- Extracts files from `.psarc` archives
- Locates and parses `song.xml`
- Generates clean `sync.json` files
- Full logging to file and console (via Loguru)
- YAML-based configuration
- Easy to extend with more extraction or analysis features

---

## 📂 Folder Structure

```plaintext
project_root/
├── resources/
│   ├── psarcs/      # Drop your .psarc files here
│   ├── output/      # Extracted sync.json and other output files
│   ├── logs/        # Log files
├── parsers/         # PSARC file parsers
├── generators/      # Sync.json file generators
├── utils/           # Logging, config, and helpers
├── config.yaml      # Application settings
└── main.py          # Entry point
```

---

## 🛠️ Installation

1. Clone the repository
2. Create and activate a virtual environment:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

Typical dependencies:
- `loguru`
- `PyYAML`

---

## ⚙️ Configuration

All settings are stored in `config.yaml`:

```yaml
log_level: INFO
input_folder: "./resources/psarcs"
output_folder: "./resources/output"
log_folder: "./resources/logs"
extract_audio: true
overwrite_output: false
```

You can control logging, extraction behaviour, and folders here.

---

## 🚀 Usage

After placing your `.psarc` files into the `resources/psarcs/` directory, run:

```bash
python main.py
```

- Output `sync.json` files will be saved in the `resources/output/` directory.
- Logs will appear under the `resources/logs/` directory.

---

## 🤝 Contributing

Pull requests and feature ideas are welcome!  
If you find bugs or want to add features (like advanced audio extraction), feel free to open an issue or submit a PR.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🧐 Future Plans

- Proper audio (`.wem`/`.ogg`) extraction
- More accurate filename restoration
- GUI frontend (optional)
- Advanced error handling and validation

