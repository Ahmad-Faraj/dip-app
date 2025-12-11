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

## Screenshots

### Home Page
<img width="1599" height="899" alt="image" src="https://github.com/user-attachments/assets/31e4a29f-1357-4f6d-b50f-2a03883c9d5f" />

### JPEG Compression
<img width="1579" height="886" alt="image" src="https://github.com/user-attachments/assets/438cee09-b3cc-4a27-bb4f-3300eeca3007" />

### Noise Reduction
<img width="1596" height="899" alt="image" src="https://github.com/user-attachments/assets/43bfef2f-f433-4cf5-8d5e-c6cd275fb8fc" />



## Algorithms

- `JPEG_Compression.py` - DCT-based JPEG compression
- `Median_Filter.py` - Median filter for salt-and-pepper noise
- `Average_Filter.py` - Average filter for image smoothing
