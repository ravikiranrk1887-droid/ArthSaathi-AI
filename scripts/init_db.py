"""
scripts/init_db.py
==================
Creates all database tables and runs the seed data script.
Run once from the project root:

    python scripts/init_db.py
"""

import sys
import os

# Make sure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created successfully.")

    print("Running seed data...")
    from scripts.seed_data import seed_all
    seed_all()
    print("Database initialised and seeded successfully!")
