#!/usr/bin/env python3
"""
Selective Matrix Data Copy
Copies specific users and room data from corrupted backup to clean database
"""

import os
import shutil
from pathlib import Path
import subprocess

def copy_user_files(source_db, target_db, users):
    """Copy user-related files from source to target database"""
    
    print(f"Copying user data from {source_db} to {target_db}")
    
    # Look for user-related SST and log files
    source_path = Path(source_db)
    target_path = Path(target_db)
    
    if not source_path.exists():
        print(f"Source database not found: {source_db}")
        return False
    
    if not target_path.exists():
        print(f"Target database not found: {target_db}")
        return False
    
    # List files in source
    print("Files in source database:")
    for file in source_path.glob("*"):
        if file.is_file():
            size = file.stat().st_size
            print(f"  {file.name}: {size} bytes")
    
    # Copy specific files that likely contain user data
    files_to_copy = []
    
    # Look for SST files (these contain the actual data)
    for sst_file in source_path.glob("*.sst"):
        if sst_file.stat().st_size > 0:  # Only copy non-empty files
            files_to_copy.append(sst_file.name)
    
    # Look for log files
    for log_file in source_path.glob("*.log"):
        if log_file.stat().st_size > 0:
            files_to_copy.append(log_file.name)
    
    print(f"Found {len(files_to_copy)} files to potentially copy:")
    for file in files_to_copy:
        print(f"  {file}")
    
    # For safety, let's first back up the current clean database
    backup_path = f"{target_db}_backup_before_import"
    if Path(backup_path).exists():
        shutil.rmtree(backup_path)
    shutil.copytree(target_db, backup_path)
    print(f"Created backup at: {backup_path}")
    
    # Copy selective files - be very careful here
    copied_files = 0
    for file_name in files_to_copy:
        source_file = source_path / file_name
        target_file = target_path / file_name
        
        try:
            # Only copy if target doesn't exist or is smaller
            if not target_file.exists() or target_file.stat().st_size < source_file.stat().st_size:
                shutil.copy2(source_file, target_file)
                print(f"  Copied: {file_name}")
                copied_files += 1
            else:
                print(f"  Skipped: {file_name} (target exists and is larger)")
        except Exception as e:
            print(f"  Error copying {file_name}: {e}")
    
    print(f"Copied {copied_files} files")
    return copied_files > 0

def repair_database_after_copy(db_path):
    """Repair database after copying files"""
    
    print(f"Repairing database: {db_path}")
    
    # Use docker to run RocksDB repair
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{db_path}:/db",
        "ubuntu:22.04",
        "bash", "-c",
        "apt-get update && apt-get install -y rocksdb-tools && ldb repair --db=/db"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Database repair successful")
            return True
        else:
            print(f"✗ Database repair failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error running repair: {e}")
        return False

def main():
    source_db = "/home/user1/runtipi/app-data/my-runtipi-apps/continuwuity/data-corrupted-backup"
    target_db = "/home/user1/runtipi/app-data/my-runtipi-apps/continuwuity/data"
    
    users_to_restore = [
        "@shawneepiano:hi.asapllc.com",
        "@admin:hi.asapllc.com", 
        "@mmeadowcroft:hi.asapllc.com",
        # Add more users as needed
    ]
    
    print("Starting selective Matrix data copy...")
    print(f"Source: {source_db}")
    print(f"Target: {target_db}")
    print(f"Users to restore: {len(users_to_restore)}")
    
    # Copy user files
    success = copy_user_files(source_db, target_db, users_to_restore)
    
    if not success:
        print("✗ File copy failed")
        return False
    
    # Repair database after copy
    success = repair_database_after_copy(target_db)
    
    if success:
        print("✓ Selective data copy completed successfully!")
    else:
        print("✗ Database repair failed")
        return False
    
    return True

if __name__ == "__main__":
    main()