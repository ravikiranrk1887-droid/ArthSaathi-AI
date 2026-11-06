import sys
import os

# Add root directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import app

# Vercel Serverless Function entrypoint
# The 'app' object is the WSGI application instance
