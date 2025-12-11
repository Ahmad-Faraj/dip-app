# Digital Image Processing Lab

Minimal web app for JPEG compression and noise reduction filters.

## Features

- **JPEG Compression**: Compress images with quality control and view size metrics
- **Noise Reduction**: Apply Median or Average filters with adjustable kernel size

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
start.bat
```

Or manually:
```bash
python app.py
python -m http.server 8000
```

3. Open http://localhost:8000

## Algorithms

- `JPEG_Compression.py` - DCT-based JPEG compression
- `Median_Filter.py` - Median filter for salt-and-pepper noise
- `Average_Filter.py` - Average filter for image smoothing
