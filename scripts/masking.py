import numpy as np
from PIL import Image

from src.geometry import viewpoint_to_pixels


def get_side_view_of_pano(image_width, image_height, heading, mask_degrees):
    right_mask_min = heading + 90 - mask_degrees / 2
    right_mask_max = heading + 90 + mask_degrees / 2
    left_mask_min = heading - 90 - mask_degrees / 2
    left_mask_max = heading - 90 + mask_degrees / 2

    right_mask_cols = np.arange(
        viewpoint_to_pixels(right_mask_min, image_width),
        viewpoint_to_pixels(right_mask_max, image_width),
        dtype=int,
    ) % image_width
    left_mask_cols = np.arange(
        viewpoint_to_pixels(left_mask_min, image_width),
        viewpoint_to_pixels(left_mask_max, image_width),
        dtype=int,
    ) % image_width

    mask = np.full((image_height, image_width, 3), True)
    mask[:, right_mask_cols, :] = False
    mask[:, left_mask_cols, :] = False
    return mask


def mask_image(image, mask):
    np_image = np.array(image)
    masked = np_image.copy()
    masked[mask] = 0
    return Image.fromarray(masked, "RGB")


if __name__ == "__main__":
    # In project root run: PYTHONPATH=. python scripts/masking.py
    mask = get_side_view_of_pano(4000, 2000, 252, 90)
    with Image.open('examples/panorama_4000.jpeg') as source_image:
        masked_image = mask_image(source_image, mask)
        masked_image.save("examples/panorama_4000_masked.jpeg", "jpeg")
