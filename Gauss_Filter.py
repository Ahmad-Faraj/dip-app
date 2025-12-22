from os import sys, makedirs
from PIL import Image
import numpy as np
import os


class GaussFilter:
    """
    Applies a Gaussian (gauss) filter to an image or array.
    """

    def __init__(self, input_path=None):
        self.input_path = input_path
        if input_path:
            try:
                self.image = Image.open(input_path).convert("L")
            except FileNotFoundError:
                print("File not found. Please provide a valid path.")
                sys.exit(1)
        else:
            self.image = None

    def _gaussian_kernel(self, size=3, sigma=None):
        if sigma is None:
            sigma = size / 6.0 if size > 1 else 0.5

        ax = np.arange(-size // 2 + 1.0, size // 2 + 1.0)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx**2 + yy**2) / (2.0 * sigma**2))
        kernel = kernel / np.sum(kernel)
        return kernel

    def gauss_filter_custom(self, image_array, size=3, method="padding", sigma=None):
        pad = size // 2
        kernel = self._gaussian_kernel(size, sigma)
        # Handle 2D (grayscale) and 3D (color) arrays differently when padding
        if image_array.ndim == 3:
            pad_width = ((pad, pad), (pad, pad), (0, 0))
        else:
            pad_width = ((pad, pad), (pad, pad))

        if method == "padding":
            padded_img = np.pad(
                image_array, pad_width, mode="constant", constant_values=0
            )
        elif method == "reflect":
            padded_img = np.pad(image_array, pad_width, mode="reflect")
        elif method == "edge":
            padded_img = np.pad(image_array, pad_width, mode="edge")
        elif method == "symmetric":
            padded_img = np.pad(image_array, pad_width, mode="symmetric")
        elif method == "crop":
            # Prepare output with channel awareness
            if image_array.ndim == 3:
                filtered_img = np.zeros(
                    (
                        image_array.shape[0] - 2 * pad,
                        image_array.shape[1] - 2 * pad,
                        image_array.shape[2],
                    ),
                    dtype=float,
                )
                for i in range(pad, image_array.shape[0] - pad):
                    for j in range(pad, image_array.shape[1] - pad):
                        window = image_array[
                            i - pad : i + pad + 1, j - pad : j + pad + 1, :
                        ]
                        # apply kernel across spatial dims and keep channels
                        filtered_img[i - pad, j - pad] = np.sum(
                            window * kernel[..., np.newaxis], axis=(0, 1)
                        )
            else:
                filtered_img = np.zeros(
                    (image_array.shape[0] - 2 * pad, image_array.shape[1] - 2 * pad),
                    dtype=float,
                )
                for i in range(pad, image_array.shape[0] - pad):
                    for j in range(pad, image_array.shape[1] - pad):
                        window = image_array[
                            i - pad : i + pad + 1, j - pad : j + pad + 1
                        ]
                        filtered_img[i - pad, j - pad] = np.sum(window * kernel)
            return filtered_img.astype(np.uint8)
        else:
            raise ValueError(
                "Invalid method. Choose from 'padding', 'reflect', 'edge', 'symmetric', 'crop'."
            )

        filtered_img = np.zeros_like(image_array, dtype=float)
        for i in range(image_array.shape[0]):
            for j in range(image_array.shape[1]):
                if image_array.ndim == 3:
                    window = padded_img[i : i + size, j : j + size, :]
                    # kernel shape -> (size,size,1) to broadcast over channels
                    vals = np.sum(window * kernel[..., np.newaxis], axis=(0, 1))
                    filtered_img[i, j] = vals
                else:
                    window = padded_img[i : i + size, j : j + size]
                    filtered_img[i, j] = np.sum(window * kernel)

        return np.clip(filtered_img, 0, 255).astype(np.uint8)

    def process_image(self, size=3, method="padding", sigma=None):
        if self.image is None:
            raise ValueError("No image loaded to process")

        image_array = np.array(self.image)
        filtered_image_array = self.gauss_filter_custom(
            image_array, size, method, sigma
        )
        filtered_image = Image.fromarray(filtered_image_array.astype(np.uint8))

        output_dir = "filtered"
        os.makedirs(output_dir, exist_ok=True)

        output_path = f"{output_dir}/{os.path.basename(self.input_path).split('.')[0]}_gauss_filtered.jpg"
        filtered_image.save(output_path)

        return filtered_image


def test_filter_on_custom_array_gauss():
    print("Enter a 2D array (as a list of lists). Example: [[1,2,3],[4,5,6],[7,8,9]]")
    user_input = input("Your 2D array: ")
    try:
        custom_array = np.array(eval(user_input))
        size = int(input("Enter the filter size (e.g., 3 for a 3x3 filter): "))
        method = input(
            "Choose an edge-handling method (padding, crop, reflect, edge, symmetric): "
        )
        sigma = input("Enter sigma (press enter to use default): ")
        sigma = float(sigma) if sigma.strip() != "" else None

        filt = GaussFilter()
        filtered = filt.gauss_filter_custom(
            custom_array, size=size, method=method, sigma=sigma
        )
        print(filtered)
    except Exception as e:
        print(f"An error occurred: {e}")


# test_filter_on_custom_array_gauss()
