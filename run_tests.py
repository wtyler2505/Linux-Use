import pytest
import sys

if __name__ == "__main__":
    # Run pytest, exiting with the appropriate status code
    sys.exit(pytest.main(["-v", "tests/"]))