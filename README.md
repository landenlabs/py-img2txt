<table border="0">
  <tr>
    <td>
      <!-- VERSION -->v1.00.00<br>
      <!-- DATE -->May-2026<br>
      macOS &nbsp;|&nbsp; Windows &nbsp;|&nbsp; Linux<br>
      <a href="https://landenlabs.com">Home</a>
    </td>
    <td>
      <a href="https://landenlabs.com">
        <img src="screens/landenlabs_400.webp" width="300" alt="LanDen Labs">
      </a>
    </td>
  </tr>
</table>

# img2txt

A cross-platform CLI that extracts text from image files using Tesseract OCR.
Accepts glob patterns, auto-scales small images for better accuracy, and writes
output to stdout or a file.

**By [LanDen Labs](https://github.com/landenlabs) (2026)**

---

## Screenshots

_(coming soon)_

---

## Features

- **Glob input patterns.** Pass one or more `--input` arguments; each may be a
  literal path or a shell glob (`*.png`, `dir/**/*.png`). Files are de-duplicated
  and processed in sorted order.
- **Auto-scale.** By default (`--scale auto`), images whose shorter side is below
  1200 px are upscaled with Lanczos before OCR — Tesseract reads small fonts
  (below ~30 px x-height) poorly without this step. Pass a numeric multiplier
  (e.g. `--scale 2`) to override, or `--scale 1` to disable.
- **Multi-file headers.** When processing more than one file, each result block is
  preceded by `===== filename =====`. Suppress with `--no-header`.
- **Output to file.** `--output FILE` collects all extracted text into a single
  file; default is stdout.
- **Tesseract options.** Pass `--lang`, `--psm`, `--oem`, and `--config` directly
  to pytesseract for full control over language, segmentation mode, and engine mode.
- **Standard CLI.** `--version`, `--help` with examples, non-zero exit code on any
  per-file error.

---

## Requirements

- Python 3.9 or later
- [Pillow](https://pillow.readthedocs.io)
- [pytesseract](https://github.com/madmaze/pytesseract)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) binary on `PATH`

```
pip install pillow pytesseract
```

Install Tesseract:
- **macOS:** `brew install tesseract`
- **Windows:** download the installer from the [Tesseract releases page](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux:** `sudo apt install tesseract-ocr`

---

## Installation

### Run from source

```bash
git clone https://github.com/landenlabs/img2txt.git
cd img2txt
python img2txt.py --help
```

### Build a standalone binary

**macOS / Linux**

```bash
pyinstaller --onefile --name img2txt img2txt.py
```

**Windows**

```powershell
pyinstaller --onefile --name img2txt img2txt.py
```

Both commands use [PyInstaller](https://pyinstaller.org) to produce a self-contained executable.

---

## Usage

### Extract text from a single image

```bash
python img2txt.py --input screenshot.png
```

### Process multiple images with a glob

```bash
python img2txt.py --input '*.png'
python img2txt.py --input 'docs/*.png' --input 'shots/*.png'
```

### Save output to a file

```bash
python img2txt.py --input '*.png' --output extracted.txt
```

### Suppress per-file banners

```bash
python img2txt.py --input '*.png' --no-header
```

### Tune Tesseract settings

```bash
# French language, PSM 4 (single column)
python img2txt.py --input doc.png --lang fra --psm 4

# Specific OCR engine mode
python img2txt.py --input doc.png --oem 1

# Disable auto-scale
python img2txt.py --input doc.png --scale 1

# Fixed 2× upscale
python img2txt.py --input doc.png --scale 2
```

### All flags

| Flag | Purpose |
| ---- | ------- |
| `--input` / `-i` | Image file or glob pattern (repeatable, required) |
| `--output` / `-o` | Write all text to FILE instead of stdout |
| `--lang` / `-l` | Tesseract language code (default: `eng`) |
| `--psm` | Page segmentation mode (default: `6`) |
| `--oem` | OCR engine mode (default: Tesseract default) |
| `--config` | Extra config string passed to Tesseract |
| `--scale` | Upscale factor or `auto` (default: `auto`) |
| `--no-header` | Suppress per-file `===== filename =====` banners |
| `--version` / `-V` | Print version and exit |
| `--help` | Show full usage and examples |

---

## Project structure

```
img2txt/
├── img2txt.py          # Main script (single-file CLI)
├── README.md
├── LICENSE
└── screens/            # Images used in this README
```

---

## License

Apache 2.0 © [LanDen Labs](https://github.com/landenlabs) 2026
