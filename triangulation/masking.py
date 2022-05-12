import numpy as np
from PIL import Image

from triangulation.helpers import viewpoint_to_pixels


def get_side_view_of_pano(image_width, image_height, heading, mask_degrees):
    """
    Generate mask to get the side view of a panorama image

    Arguments:
    image_width: int = Panorama image width in pixels
    image_height: int = Panorama image height in pixels
    heading: Number = Car heading in degrees
    mask_degrees: Number = Mask size in degrees. The mask will be applied to the front and back of the image, meaning that a mask
    of 180 degrees will obscure the entire image.

    Returns:
    npt.NDArray[(image_height, image_width, 3), bool]
    """
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
    """
    Applies supplied mask to supplied image

    Arguments:
    image: PIL.Image
    mask: npt.NDArray[(~Shape), bool] where shape matches the image dimensions

    Returns:
    PIL.Image
    """
    np_image = np.array(image)
    masked = np_image.copy()
    masked[mask] = 0
    return Image.fromarray(masked, "RGB")


if __name__ == "__main__":
    # In project root run: PYTHONPATH=. python scripts/masking.py
    # Panorama used in example is available at:
    # https://api.data.amsterdam.nl/panorama/panoramas/TMX7316010203-001886_pano_0000_002013/
    mask = get_side_view_of_pano(4000, 2000, 252, 90)
    with Image.open('../examples/panorama_4000.jpeg') as source_image:
        masked_image = mask_image(source_image, mask)
        masked_image.save("../examples/panorama_4000_masked.jpeg", "jpeg")
