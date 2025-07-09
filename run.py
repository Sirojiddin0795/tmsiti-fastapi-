#!/usr/bin/env python3
"""
TMSITI FastAPI Server Startup Script
This script ensures proper environment setup and starts the FastAPI server
"""

import os
import sys
import subprocess
from pathlib import Path

# Set SQLite database URL before importing anything
os.environ["DATABASE_URL"] = "sqlite:///./tmsiti.db"

# Remove any PostgreSQL environment variables that might interfere
for key in ["PGDATABASE", "PGHOST", "PGPORT", "PGUSER", "PGPASSWORD"]:
    if key in os.environ:
        del os.environ[key]

def main():
    """Main startup function"""
    print("TMSITI FastAPI Server")
    print("=" * 50)
    
    # Check if database exists, if not create it
    if not Path("tmsiti.db").exists():
        print("Database not found. Initializing...")
        try:
            subprocess.run([sys.executable, "create_tables.py"], check=True)
            print("✓ Database initialized successfully!")
        except subprocess.CalledProcessError as e:
            print(f"✗ Database initialization failed: {e}")
            return 1
    else:
        print("✓ Database found")
    
    # Start the FastAPI server
    print("Starting FastAPI server...")
    print("Access the API at: http://localhost:5000")
    print("API Documentation: http://localhost:5000/docs")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "5000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Server failed to start: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())