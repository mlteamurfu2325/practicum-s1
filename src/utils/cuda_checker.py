"""Module to provide function to check if we can use a CUDA GPU."""

import ctypes


def check_cuda():
    """
    Check if CUDA GPUs are available without importing torch or tensorflow

    Returns
    -------
    bool
        True if a CUDA GPU is available, False otherwise
    """
    try:
        ctypes.cdll.LoadLibrary("libcuda.so")
        return True
    except OSError:
        return False
