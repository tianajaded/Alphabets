import numpy as np


def pixel_count_complexity(picture):
    """
    Computes number of unique pixel values in the image.

    Inputs:
        picture: 2D NumPy array representing the image.

    Returns:
        complexity: Number of unique pixel values in the image.
    """
    return len(np.unique(picture))
