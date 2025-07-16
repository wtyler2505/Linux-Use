import random
from uiautomation import Control

def random_point_within_bounding_box(node: Control, scale_factor: float = 1.0, window_size: tuple[int, int] = None) -> tuple[int, int]:
    """
    Generate a random point within a scaled-down bounding box, centered within the window boundaries.

    Args:
        node (Control): The node with a bounding rectangle
        scale_factor (float, optional): The factor to scale down the bounding box. Defaults to 1.0.
        window_size (tuple[int, int], optional): The size of the window. Defaults to None.

    Returns:
        tuple: A random point (x, y) within the scaled-down bounding box, centered within the window boundaries
    """
    box = node.BoundingRectangle
    scaled_width = int(box.width() * scale_factor)
    scaled_height = int(box.height() * scale_factor)
    scaled_left = box.left + (box.width() - scaled_width) // 2
    scaled_top = box.top + (box.height() - scaled_height) // 2

    # Calculate center point of bounding box within window boundaries
    if window_size:
        intersection_x = max(0, min(scaled_left, window_size[0] - scaled_width))
        intersection_y = max(0, min(scaled_top, window_size[1] - scaled_height))
        center_x = intersection_x + scaled_width / 2
        center_y = intersection_y + scaled_height / 2
    else:
        center_x = scaled_left + scaled_width / 2
        center_y = scaled_top + scaled_height / 2

    # Generate random point around center point
    x = random.randint(int(center_x - scaled_width / 2), int(center_x + scaled_width / 2))
    y = random.randint(int(center_y - scaled_height / 2), int(center_y + scaled_height / 2))
    return (x, y)