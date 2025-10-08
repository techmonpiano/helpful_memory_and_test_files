#!/usr/bin/env python3
"""
Matrix Data Import Tool for RocksDB
Imports users and rooms into a clean Continuwuity database
"""

import rocksdb
import json
import sys
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

def import_users_to_rocksdb(db_path):
    """Import users into RocksDB database"""
    print(f"Opening database: {db_path}")
    
    # Open database
    opts = rocksdb.Options()
    opts.create_if_missing = False
    opts.error_if_exists = False
    
    try:
        db = rocksdb.DB(db_path, opts)
        print("Database opened successfully")
    except Exception as e:
        print(f"Error opening database: {e}")
        return False
    
    # Import users
    print("Importing users...")
    for user in USERS_TO_IMPORT:
        try:
            # Create user key-value pairs in RocksDB format
            user_key = f"userid_{user['user_id']}"
            user_data = {
                "localpart": user["localpart"],
                "server_name": user["server_name"],
                "created_ts": user["created_ts"]
            }
            
            # Store user data
            db.put(user_key.encode(), json.dumps(user_data).encode())
            print(f"  Imported user: {user['user_id']}")
            
            # Also store localpart mapping for login
            localpart_key = f"localpart_{user['localpart']}"
            db.put(localpart_key.encode(), user['user_id'].encode())
            
        except Exception as e:
            print(f"  Error importing user {user['user_id']}: {e}")
    
    print("Users import completed")
    return True

def import_rooms_to_rocksdb(db_path):
    """Import rooms into RocksDB database"""
    print(f"Opening database: {db_path}")
    
    # Open database
    opts = rocksdb.Options()
    opts.create_if_missing = False
    opts.error_if_exists = False
    
    try:
        db = rocksdb.DB(db_path, opts)
        print("Database opened successfully")
    except Exception as e:
        print(f"Error opening database: {e}")
        return False
    
    # Import rooms
    print("Importing rooms...")
    for room in ROOMS_TO_IMPORT:
        try:
            # Create room key-value pairs in RocksDB format
            room_key = f"roomid_{room['room_id']}"
            room_data = {
                "room_version": room["room_version"],
                "creator": room["creator"],
                "created_ts": room["created_ts"]
            }
            
            # Store room data
            db.put(room_key.encode(), json.dumps(room_data).encode())
            print(f"  Imported room: {room['room_id']}")
            
        except Exception as e:
            print(f"  Error importing room {room['room_id']}: {e}")
    
    print("Rooms import completed")
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 import_matrix_data.py <database_path>")
        print("Example: python3 import_matrix_data.py /var/lib/matrix-conduit/")
        sys.exit(1)
    
    db_path = sys.argv[1]
    
    if not Path(db_path).exists():
        print(f"Database path does not exist: {db_path}")
        sys.exit(1)
    
    print("Starting Matrix data import...")
    print(f"Target database: {db_path}")
    
    # Import users
    success = import_users_to_rocksdb(db_path)
    if not success:
        print("User import failed")
        sys.exit(1)
    
    # Import rooms
    success = import_rooms_to_rocksdb(db_path)
    if not success:
        print("Room import failed") 
        sys.exit(1)
    
    print("Matrix data import completed successfully!")

if __name__ == "__main__":
    main()