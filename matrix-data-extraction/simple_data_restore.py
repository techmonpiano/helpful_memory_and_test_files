#!/usr/bin/env python3
"""
Simple Matrix Data Restore
Creates a manual data restoration by copying key database files
"""

import os
import shutil
from pathlib import Path

def restore_from_backup():
    """Copy the entire corrupted database to see if we can extract users"""
    
    source_db = "/home/user1/runtipi/app-data/my-runtipi-apps/continuwuity/data-corrupted-backup"
    target_db = "/home/user1/runtipi/app-data/my-runtipi-apps/continuwuity/data"
    backup_clean = f"{target_db}_clean_backup"
    
    print("Simple data restore approach...")
    
    # First, backup the clean database
    if Path(backup_clean).exists():
        shutil.rmtree(backup_clean)
    
    print(f"Backing up clean database to: {backup_clean}")
    shutil.copytree(target_db, backup_clean)
    
    # Now, let's try copying specific files from corrupted backup
    # that might contain user data but aren't corrupted
    
    source_path = Path(source_db)
    target_path = Path(target_db)
    
    print("\nFiles in corrupted backup:")
    corrupted_files = list(source_path.glob("*"))
    for file in corrupted_files:
        if file.is_file():
            size = file.stat().st_size
            print(f"  {file.name}: {size:,} bytes")
    
    print("\nFiles in clean database:")
    clean_files = list(target_path.glob("*"))
    for file in clean_files:
        if file.is_file():
            size = file.stat().st_size
            print(f"  {file.name}: {size:,} bytes")
    
    # Instead of copying files, let's create a hybrid approach
    # Copy the MANIFEST and CURRENT files from clean, but try some data files from backup
    
    print("\nHybrid restoration approach:")
    
    # Files that are safe to copy from backup (contain user data)
    safe_to_copy = []
    
    # Look for SST files from backup that might contain user data
    for sst_file in source_path.glob("*.sst"):
        if sst_file.stat().st_size > 1000:  # Reasonable size
            safe_to_copy.append(sst_file.name)
    
    # Copy the metadata files from clean database (keep structure intact)
    # But try to add some data files from backup
    
    copied_count = 0
    for file_name in safe_to_copy[:3]:  # Only try first 3 SST files to be safe
        source_file = source_path / file_name
        target_file = target_path / file_name
        
        # Check if this file already exists in clean database
        if not target_file.exists():
            try:
                shutil.copy2(source_file, target_file)
                print(f"  Copied data file: {file_name}")
                copied_count += 1
            except Exception as e:
                print(f"  Failed to copy {file_name}: {e}")
        else:
            print(f"  Skipped {file_name} (already exists)")
    
    print(f"\nCopied {copied_count} data files from backup")
    
    # Create a summary of what we did
    restore_summary = f"""
Restoration Summary:
- Clean database backed up to: {backup_clean}
- Attempted to copy {len(safe_to_copy)} data files from corrupted backup
- Successfully copied {copied_count} files
- Database structure preserved from clean version
- Added data files from backup that might contain users

Next steps:
1. Start Continuwuity and check if users appear
2. If database corruption occurs, restore from {backup_clean}
3. If users appear, verify they can log in
"""
    
    print(restore_summary)
    
    # Write summary to file
    with open("/home/user1/matrix-data-extraction/restore_summary.txt", "w") as f:
        f.write(restore_summary)
    
    return True

def main():
    print("Starting simple Matrix data restore...")
    
    success = restore_from_backup()
    
    if success:
        print("\n✓ Data restore attempt completed!")
        print("Try starting Continuwuity to see if users are restored")
    else:
        print("\n✗ Restore failed")
    
    return success

if __name__ == "__main__":
    main()