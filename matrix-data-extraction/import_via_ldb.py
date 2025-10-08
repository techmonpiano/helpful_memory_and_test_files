#!/usr/bin/env python3
"""
Matrix Data Import using LDB tools
Uses RocksDB command-line tools to import data
"""

import os
import subprocess
import json
from pathlib import Path

# Matrix users to import
USERS_TO_IMPORT = [
    {"user_id": "@shawneepiano:hi.asapllc.com", "localpart": "shawneepiano", "server_name": "hi.asapllc.com", "created_ts": 1724000009000},
    {"user_id": "@admin:hi.asapllc.com", "localpart": "admin", "server_name": "hi.asapllc.com", "created_ts": 1720086400000},
    {"user_id": "@mmeadowcroft:hi.asapllc.com", "localpart": "mmeadowcroft", "server_name": "hi.asapllc.com", "created_ts": 1720086400000},
    {"user_id": "@amanda:hi.asapllc.com", "localpart": "amanda", "server_name": "hi.asapllc.com", "created_ts": 1720086400000},
    {"user_id": "@bschwalm:hi.asapllc.com", "localpart": "bschwalm", "server_name": "hi.asapllc.com", "created_ts": 1720086400000},
    {"user_id": "@tkennedy:hi.asapllc.com", "localpart": "tkennedy", "server_name": "hi.asapllc.com", "created_ts": 1720086400000},
    {"user_id": "@mschwalm:hi.asapllc.com", "localpart": "mschwalm", "server_name": "hi.asapllc.com", "created_ts": 1720086400000},
    {"user_id": "@pbschwalm:hi.asapllc.com", "localpart": "pbschwalm", "server_name": "hi.asapllc.com", "created_ts": 1720086400000},
    {"user_id": "@ellie:hi.asapllc.com", "localpart": "ellie", "server_name": "hi.asapllc.com", "created_ts": 1720086400000},
    {"user_id": "@ellie2:hi.asapllc.com", "localpart": "ellie2", "server_name": "hi.asapllc.com", "created_ts": 1720086400000},
    {"user_id": "@support:hi.asapllc.com", "localpart": "support", "server_name": "hi.asapllc.com", "created_ts": 1720086400000},
]

# Matrix rooms to import (basic room structure)
ROOMS_TO_IMPORT = [
    {"room_id": "!hFytmqvCe0h5Qg3iKA:hi.asapllc.com", "room_version": "10", "creator": "@admin:hi.asapllc.com", "created_ts": 1720086400000},
    {"room_id": "!aBcDeFgHiJkLmNoPqR:hi.asapllc.com", "room_version": "10", "creator": "@admin:hi.asapllc.com", "created_ts": 1720086400000},
]

def create_import_files():
    """Create data files for import using ldb commands"""
    
    print("Creating import data files...")
    
    # Create users import file
    with open("/tmp/users_import.txt", "w") as f:
        for user in USERS_TO_IMPORT:
            # Based on Conduit/Continuwuity key patterns
            user_key = f"userid\x00{user['user_id']}"
            user_data = json.dumps({
                "localpart": user["localpart"],
                "server_name": user["server_name"], 
                "created_ts": user["created_ts"]
            })
            
            # Write in ldb put format: PUT key value
            f.write(f"PUT {user_key} {user_data}\n")
            
            # Also create localpart mapping
            localpart_key = f"localpart\x00{user['localpart']}"
            f.write(f"PUT {localpart_key} {user['user_id']}\n")
    
    # Create rooms import file
    with open("/tmp/rooms_import.txt", "w") as f:
        for room in ROOMS_TO_IMPORT:
            # Based on Conduit/Continuwuity key patterns
            room_key = f"roomid\x00{room['room_id']}"
            room_data = json.dumps({
                "room_version": room["room_version"],
                "creator": room["creator"],
                "created_ts": room["created_ts"]
            })
            
            # Write in ldb put format: PUT key value
            f.write(f"PUT {room_key} {room_data}\n")
    
    print("Import files created:")
    print("  /tmp/users_import.txt")
    print("  /tmp/rooms_import.txt")

def import_data_with_ldb(db_path):
    """Import data using ldb tools"""
    
    print(f"Importing data to database: {db_path}")
    
    # Import users
    try:
        cmd = ["ldb", "--db", db_path, "batch", "/tmp/users_import.txt"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Users imported successfully")
        else:
            print(f"✗ Users import failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: ldb command not found")
        return False
    
    # Import rooms  
    try:
        cmd = ["ldb", "--db", db_path, "batch", "/tmp/rooms_import.txt"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Rooms imported successfully")
        else:
            print(f"✗ Rooms import failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: ldb command not found")
        return False
    
    return True

def main():
    db_path = "/var/lib/matrix-conduit"
    
    if not Path(db_path).exists():
        print(f"Database path does not exist: {db_path}")
        return False
    
    print("Starting Matrix data import using ldb tools...")
    
    # Create import files
    create_import_files()
    
    # Import data
    success = import_data_with_ldb(db_path)
    
    if success:
        print("✓ Matrix data import completed successfully!")
    else:
        print("✗ Import failed")
        return False
    
    # Cleanup
    os.remove("/tmp/users_import.txt")
    os.remove("/tmp/rooms_import.txt")
    
    return True

if __name__ == "__main__":
    main()