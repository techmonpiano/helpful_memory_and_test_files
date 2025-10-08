# Matrix Server SST Files Investigation Session
**Date**: August 25, 2025  
**Topic**: Investigation of Missing SST Files (001361, 001362, 001365) in Matrix Server Context  
**Session Type**: Research/Discovery Session

## Initial Query
User asked to search online for Matrix server issues regarding missing SST files with specific numbers: 001361, 001362, 001365

## Investigation Process

### Search Strategy
1. **Initial Search**: Searched for "matrix server missing SST files 001361 001362 001365"
   - Result: No direct matches found for these specific file numbers in Matrix server context

2. **Broader SST Search**: Explored general SST file information
   - Found SST file format documentation
   - Discovered SST relates to various file types and databases

3. **Database Context Search**: Investigated SST in database systems
   - Found GitHub issue #1907 in Magma project containing these exact numbers
   - Numbers appeared as log line identifiers, not file names

## Key Findings

### 1. Numbers Were Not Matrix SST Files
- **001361, 001362, 001365** were actually **log line numbers** from a Magma project GitHub issue
- These appeared in authentication error logs for Magma Access Gateway configuration
- No connection found to Matrix server SST files

### 2. SST Files Explained
**SST = Sorted String Table**

#### What Are SST Files?
- Core storage format for RocksDB databases
- Contain key-value pairs sorted by key
- Immutable (read-only) once written
- Named with sequential numbers (e.g., 000001.sst, 000002.sst)

#### RocksDB Architecture
- **LSM-tree structure** (Log-Structured Merge-tree)
- Files organized in levels:
  - L0: Recently flushed memtable data
  - L1-L6: Progressively larger, more compacted levels
- New data creates new SST files rather than modifying existing ones

#### Applications Using RocksDB/SST Files
- Matrix Synapse servers (for state database)
- Kafka Streams
- MySQL with MyRocks storage engine
- Various blockchain implementations

## Potential Matrix Server SST Issues

If someone encounters missing SST files in a Matrix server:

### Symptoms
- Error messages about missing files like "001361.sst not found"
- Database manifest references files that don't exist on disk
- Server fails to start or crashes

### Root Causes
1. Database corruption
2. Incomplete backup/restore
3. Disk space issues during compaction
4. Accidental file deletion
5. Filesystem corruption

### Recovery Options
1. **Restore from backup** (preferred)
2. **Database repair tools** (if available)
3. **Rebuild from scratch** (last resort)
4. Check RocksDB logs for recovery options

## Search Results Summary

### Relevant Links Found
- RocksDB SST format documentation
- Percona XtraDB Cluster SST error diagnostics
- RocksDB GitHub issue #9419 about deleted SST files
- General Matrix server documentation (no SST references)

### Irrelevant But Discovered
- Magma project issue #1907 (contained the numbers as log lines)
- SST (Serverless Stack) framework documentation
- Sea Surface Temperature (SST) data files

## Lessons Learned

1. **Context Matters**: Numbers that appear to be file identifiers might actually be log line numbers or other identifiers
2. **SST File Association**: SST files are strongly associated with RocksDB, not specifically Matrix servers
3. **Matrix Database Options**: Matrix Synapse can use various databases (PostgreSQL, SQLite, RocksDB), and SST files only apply when using RocksDB

## Troubleshooting Recommendations

For actual Matrix server SST file issues:

1. **Verify Database Type**
   ```bash
   # Check Matrix Synapse configuration
   grep -i database homeserver.yaml
   ```

2. **Check RocksDB Logs**
   ```bash
   # Look for RocksDB-specific errors
   journalctl -u matrix-synapse | grep -i rocksdb
   ```

3. **List Actual SST Files**
   ```bash
   # If using RocksDB, check the database directory
   ls -la /var/lib/matrix-synapse/rocksdb/*.sst
   ```

4. **Validate Database Integrity**
   - Use RocksDB's built-in tools if available
   - Consider running consistency checks

## Session Outcome

**Result**: Successfully identified that the queried numbers were not related to Matrix server SST files, but rather log line numbers from an unrelated project. Provided comprehensive information about what SST files actually are and their relationship to RocksDB databases.

**Value Added**: 
- Clarified the nature of SST files
- Explained RocksDB architecture
- Provided troubleshooting guidance for actual SST file issues
- Prevented potential confusion about the source of the numbers

## Additional Resources

- [RocksDB SST Format Tutorial](https://github.com/facebook/rocksdb/wiki/A-Tutorial-of-RocksDB-SST-formats)
- [Creating and Ingesting SST Files](https://github.com/facebook/rocksdb/wiki/creating-and-ingesting-sst-files)
- [Matrix Synapse Documentation](https://matrix-org.github.io/synapse/latest/)
- [RocksDB Recovery Documentation](https://github.com/facebook/rocksdb/wiki/RocksDB-Recovery)

---
*This memory file documents a research session where initial assumptions about missing Matrix server SST files were corrected through systematic investigation.*