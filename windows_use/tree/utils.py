import random
from uiautomation import Control

def random_point_within_bounding_box(node:Control)->tuple[int,int]:
    """
    Generate a random point within a bounding box.

    Args:
        box (BoundingBox): The bounding box

    Returns:
        tuple: A random point (x, y) within the bounding box
    """
    box = node.BoundingRectangle
    x = random.randint(box.left, box.left + box.width())
    y = random.randint(box.top, box.top + box.height())
    return (x, y)