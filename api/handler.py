"""
Vercel handler file that imports the FastAPI app.
This handles the import differences between local and serverless environments.
"""

import sys
import os

# Add the project root to the Python path for absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try to import the app
try:
    # First try absolute import (for Vercel)
    from api.main import app
except ImportError:
    # Fallback to relative import (for local development)
    from main import app

# Import mangum only when needed
try:
    from mangum import Mangum
    # Mangum handler for Vercel serverless functions
    handler = Mangum(app)
except ImportError:
    # If mangum is not available, just use the app directly
    handler = app 