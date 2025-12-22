from flask import Flask, request, jsonify
from JPEG_Compression import Compressor
from Median_Filter import MedianFilter
from Average_Filter import AverageFilter
from Gauss_Filter import GaussFilter
from MinMax_Filter import MinMaxFilter
from PIL import Image
import numpy as np
import io
import base64
import tempfile
import os

app = Flask(__name__)


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/compress", methods=["POST"])
def compress():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files["file"]
    quality = int(request.form.get("quality", 50))

    # Create compressed directory if it doesn't exist
    os.makedirs("compressed", exist_ok=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        original_size = os.path.getsize(tmp_path)
        # Convert Windows path to forward slashes for Compressor
        tmp_path_normalized = tmp_path.replace("\\", "/")
        compressor = Compressor(tmp_path_normalized, quality=quality)
        compressed_img = compressor.compress()

        # Compressor saves to compressed/ directory, read it back
        compressed_filename = (
            os.path.basename(tmp_path).split(".")[0] + "_compressed.jpg"
        )
        compressed_path = os.path.join("compressed", compressed_filename)
        compressed_size = os.path.getsize(compressed_path)

        with open(compressed_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()

        ratio = round(((original_size - compressed_size) / original_size) * 100, 2)

        os.unlink(tmp_path)
        os.unlink(compressed_path)

        return jsonify(
            {
                "original_size": original_size,
                "compressed_size": compressed_size,
                "compression_percentage": ratio,
                "compressed_image": f"data:image/png;base64,{img_data}",
            }
        )
    except Exception as e:
        os.unlink(tmp_path)
        return jsonify({"error": str(e)}), 500


@app.route("/filter", methods=["POST"])
def filter_image():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files["file"]
    filter_type = request.form.get("filter_type", "Median Filter")
    kernel_size = int(request.form.get("kernel_size", 3))
    method = request.form.get("method", "padding").lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        if filter_type == "Median Filter":
            mf = MedianFilter(tmp_path)
            img_array = np.array(Image.open(tmp_path))
            filtered = mf.median_filter_custom(
                img_array, size=kernel_size, method=method
            )
        elif filter_type == "Average Filter":
            af = AverageFilter(tmp_path)
            img_array = np.array(Image.open(tmp_path))
            filtered = af.average_filter_custom(
                img_array, size=kernel_size, method=method
            )
        elif filter_type == "Gauss Filter":
            gf = GaussFilter(tmp_path)
            img_array = np.array(Image.open(tmp_path))
            # optional sigma can be passed via form 'sigma'
            sigma_val = request.form.get("sigma")
            sigma = float(sigma_val) if sigma_val is not None else None
            filtered = gf.gauss_filter_custom(
                img_array, size=kernel_size, method=method, sigma=sigma
            )
        elif filter_type == "Min-Max Filter":
            mm = MinMaxFilter(tmp_path)
            img_array = np.array(Image.open(tmp_path))
            mode = request.form.get("mode", "min").lower()
            filtered = mm.min_max_filter_custom(
                img_array, size=kernel_size, mode=mode, method=method
            )
        else:
            os.unlink(tmp_path)
            return jsonify({"error": f"{filter_type} not implemented"}), 400

        filtered_img = Image.fromarray(filtered.astype(np.uint8))
        buf = io.BytesIO()
        filtered_img.save(buf, format="PNG")
        img_data = base64.b64encode(buf.getvalue()).decode()

        os.unlink(tmp_path)

        return jsonify({"filtered_image": f"data:image/png;base64,{img_data}"})
    except Exception as e:
        os.unlink(tmp_path)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
