# Synapse Rate Limiting Configuration Guide

## Overview
When importing large amounts of messages into Matrix Synapse, the default rate limits will cause 429 "Too Many Requests" errors. This guide shows how to temporarily increase rate limits for bulk operations.

## Configuration File Location
- **File**: `homeserver.yaml` 
- **Docker path**: `/opt/synapse/data/homeserver.yaml` (inside container)
- **Host mount**: Varies by deployment (check docker-compose.yml)

## Rate Limiting Section
```yaml
rc_message:
  per_second: 10      # Default: 0.2 (allow 10 messages per second instead of 0.2)
  burst_count: 1000   # Default: 10 (allow bursts of 1000 instead of 10)

rc_registration:
  per_second: 0.17
  burst_count: 3

rc_login:
  address:
    per_second: 0.17
    burst_count: 3
  account:
    per_second: 0.17
    burst_count: 3
  failed_attempts:
    per_second: 0.17
    burst_count: 3
```

## Steps for Bulk Import

### 1. Backup Original Configuration
```bash
sudo cp homeserver.yaml homeserver.yaml.backup
```

### 2. Modify Rate Limits
Edit `homeserver.yaml` and change:
```yaml
rc_message:
  per_second: 10      # Increased from 0.2
  burst_count: 1000   # Increased from 10
```

### 3. Restart Synapse
```bash
# Docker Compose
docker-compose restart synapse

# Direct Docker
docker restart synapse

# Systemd
sudo systemctl restart matrix-synapse
```

### 4. Run Import
Execute your import script while high limits are active.

### 5. Restore Original Configuration
```bash
sudo cp homeserver.yaml.backup homeserver.yaml
```

### 6. Restart Again
```bash
docker-compose restart synapse
```

## Important Notes
- **Always backup** the original config before modifications
- **Temporary only**: High rate limits should not be permanent for security
- **Monitor resources**: High rate limits can stress the server
- **Database direct insert**: For very large imports, consider database direct insertion to bypass rate limits entirely

## Troubleshooting
- **Config errors**: Check `docker logs synapse` for syntax errors
- **Permission issues**: Ensure user has write access to config file
- **Container issues**: Verify container can read the modified config

## Alternative: Database Direct Insert
For massive imports (5000+ messages), direct database insertion bypasses rate limits:
- Insert directly into `events` and `event_json` tables
- Use proper event IDs, stream ordering, and timestamps
- Restart Synapse after import to refresh caches

Last updated: 2025-08-28