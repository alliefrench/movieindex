#!/usr/bin/env python3
"""
Development server script for Poetry.
Usage: poetry run python scripts/dev.py
"""

import os
import subprocess
import sys


def run_dev_server():
    """Run the development server with uvicorn."""
    print("🚀 Starting development server with Poetry...")

    # Change to project directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Run uvicorn with reload
    cmd = ["uvicorn", "api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Development server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_dev_server()
