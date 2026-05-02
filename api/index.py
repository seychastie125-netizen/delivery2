# Vercel entry point — re-exports the Flask app from server/app.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from server.app import app

# Vercel expects the WSGI callable to be named `app`
