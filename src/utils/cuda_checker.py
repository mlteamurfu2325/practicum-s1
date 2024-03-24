"""Module to provide a function to check if a CUDA GPU is available."""

import ctypes


def check_cuda() -> bool:
    """
    Check if CUDA GPUs are available without importing torch or tensorflow.

    Returns:
        bool: True if a CUDA GPU is available, False otherwise.
    """
    try:
        ctypes.cdll.LoadLibrary("libcuda.so")
        return True
    except OSError:
        return False
