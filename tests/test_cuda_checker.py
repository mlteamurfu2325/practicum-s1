"""Test src/utils/cuda_checker.py"""

from unittest.mock import patch

from src.utils.cuda_checker import check_cuda


def test_check_cuda_available():
    """Test that check_cuda returns True if CUDA is available.""" ""
    with patch("ctypes.cdll.LoadLibrary", return_value=True):
        assert check_cuda() is True


def test_check_cuda_not_available():
    """Test that check_cuda returns False if CUDA is not available.""" ""
    with patch("ctypes.cdll.LoadLibrary", side_effect=OSError):
        assert check_cuda() is False
