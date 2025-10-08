# Matrix Message Export/Import Research Session
**Date**: August 18, 2025  
**Session Focus**: Exploring Matrix/Element message export capabilities and import solutions

---

## Element Built-in Export Capabilities

### Export Feature (Available since Element 1.9.1)
- **Access**: Room Info → "Export Chat"
- **Formats**: HTML, Plain Text, JSON
- **Scope Options**:
  - Current timeline
  - Entire timeline 
  - Specific number of messages
- **Includes**: Attachments, room summary, light mode formatting
- **Limitation**: Export only - no built-in import functionality

### Encrypted Messages
- **Key Export**: Settings → Security & Privacy → Encryption → Export E2E room keys
- **Purpose**: Backup for message decryption, not message content
- **Import**: Can import keys for decryption, not messages themselves

---

## Matrix Server-Level Export (Synapse)

### Individual User Export (Admin Required)
```bash
python -m synapse.app.admin_cmd -c homeserver.yaml export-data @user:server.com --output-directory /path/to/export
```

### Complete Server Backup Components
- **Database**: PostgreSQL (`pg_dump`) or SQLite backup
- **Media Repository**: `/matrix/media_store/` directory
- **Configuration**: `homeserver.yaml`
- **Signing Keys**: `signing.key`

### Database Backup Examples
```bash
# PostgreSQL
pg_dump synapse_db > matrix_backup.sql

# SQLite
cp homeserver.db matrix_backup.db

# Docker deployment
docker exec --env-file=/matrix/postgres/env-postgres-psql matrix-postgres pg_dumpall -h matrix-postgres | gzip -c > /matrix/postgres.sql.gz
```

---

## Import Limitations & Current State

### Element Client Limitations
- ❌ No built-in message import feature
- ❌ Cannot import exported JSON/HTML back into rooms
- ❌ No room history recreation in UI
- ✅ Only E2E key import available

### Synapse API Status
- **Feature Request**: Import/export API exists (#3716) but not implemented
- **Admin API**: Limited to user management, not message import
- **Current Workarounds**: Custom bot scripts only

---

## GitHub Projects for Matrix Import/Export

### 1. matrix-copy-room-history (aspacca)
**Repository**: `github.com/aspacca/matrix-copy-room-history`

**Features**:
- Imports Element JSON exports to new Matrix rooms
- Uses Matrix Application Service bridge
- Handles user membership and invitations
- Preserves message content (new timestamps)

**Requirements**:
- Matrix server admin access
- Node.js/npm
- Application service registration
- Environment variables: INVITER, DOMAIN, HOMESERVER_URL, ELEMENT_EXPORT_FOLDER

**Setup Process**:
1. Clone repository and run `npm install`
2. Create JSON mapping file (source room → destination room)
3. Create destination room manually
4. Configure environment variables
5. Register application service with Synapse
6. Run import script

**Limitations**:
- Messages get new timestamps
- Requires server admin privileges
- Same-server migration only

### 2. matrix-archive (osteele)
**Repository**: `github.com/osteele/matrix-archive`

**Features**:
- Direct Matrix server export/import for archival
- Batch processing (1000 events at a time)
- Multiple export formats: HTML, JSON, YAML, text
- MongoDB storage backend
- Image message detection and URL extraction

**Requirements**:
- Python/pipenv
- MongoDB instance
- Matrix user credentials
- Environment variables: MATRIX_USER, MATRIX_PASSWORD, MATRIX_ROOM_IDS

**Commands**:
```bash
# Import messages to database
pipenv run import

# Export to file
pipenv run export filename.html

# List room IDs
pipenv run list
```

**Use Case**: Research, archival, and preservation of Matrix conversations

### 3. slack-matrix-migration (Awesome-Technologies)
**Repository**: `github.com/Awesome-Technologies/slack-matrix-migration`

**Features**:
- Complete Slack to Matrix migration
- Imports users, channels, conversations
- Recommended for fresh/empty Synapse instances
- Supports federated setups

**Best For**: Full platform migration scenarios

---

## Migration Workflows

### Workflow A: Element Export → New Room (Same Server)
**Requirements**: Matrix server admin access

1. **Export from Element**:
   - Room Info → Export Chat → JSON format
   - Save export file locally

2. **Setup matrix-copy-room-history**:
   - Clone: `git clone https://github.com/aspacca/matrix-copy-room-history`
   - Install: `npm install`
   - Configure environment variables

3. **Prepare Migration**:
   - Create destination room manually
   - Create JSON mapping file
   - Register application service

4. **Execute Import**:
   - Run import script
   - Monitor user invitations and joining
   - Verify message history

**Pros**: Uses Element's native export, preserves user membership  
**Cons**: Requires admin access, new timestamps, same-server only

### Workflow B: Direct Server-to-Server Export
**Requirements**: Matrix credentials on both servers

1. **Export with matrix-archive**:
   - Setup MongoDB and Python environment
   - Configure MATRIX_USER, MATRIX_PASSWORD, MATRIX_ROOM_IDS
   - Run: `pipenv run import` then `pipenv run export filename.json`

2. **Import to Destination**:
   - Setup matrix-archive on destination server
   - Import JSON data to new MongoDB instance
   - Create rooms and restore message history

**Pros**: Cross-server capable, preserves metadata  
**Cons**: Requires credentials on both servers, complex setup

### Workflow C: Public Server → Private Server
**Scenario**: No admin access on source, admin access on destination

1. **Element Export** (room-by-room):
   - Export each room individually via Element
   - Collect all JSON exports

2. **Batch Processing**:
   - Use matrix-copy-room-history on destination server
   - Process multiple room exports
   - Recreate room structure manually

**Pros**: Works with public servers  
**Cons**: Manual room creation, limited by Element's export scope

---

## Technical Considerations

### Matrix Specification Proposals
- **MSC2716**: Incrementally importing history into existing rooms
- **Status**: Allows Application Services to specify event parents and timestamps
- **Impact**: Enables better historical message insertion

### Authentication & Security
- **Application Services**: Require homeserver registration
- **Bot Tokens**: Need appropriate permissions for room joining/messaging
- **Rate Limiting**: Consider API rate limits for large imports

### Data Integrity
- **Timestamps**: Most tools assign new timestamps to imported messages
- **User Attribution**: Messages may appear from bot users, not original senders
- **Encryption**: Encrypted rooms require additional key management

---

## Recommendations

### For Individual Users
1. **Backup Strategy**: Use Element export for personal archival
2. **Migration**: Contact server admins for cross-server moves
3. **Alternative**: Keep exported files as external reference

### For Server Administrators
1. **Same-Server**: Use `matrix-copy-room-history` for room consolidation
2. **Cross-Server**: Use `matrix-archive` for full migration projects
3. **Testing**: Always test on non-production servers first

### For Organizations
1. **Platform Migration**: Consider `slack-matrix-migration` for Slack transitions
2. **Backup Strategy**: Implement regular database backups
3. **Documentation**: Maintain export procedures for compliance

---

## Future Developments

### Pending Features
- Import/export API in Synapse (Issue #3716)
- Native Element import functionality
- Improved timestamp preservation
- Better cross-server migration tools

### Community Tools
- Additional bot frameworks emerging
- MSC2716 implementation progress
- Third-party migration services

---

## Session Summary

**Key Findings**:
- Element export is well-developed but import is limited
- GitHub projects provide workable solutions with admin access
- Server-level tools offer more comprehensive migration options
- Cross-server migration remains complex but possible

**Best Current Solution**: `matrix-copy-room-history` for Element export imports, `matrix-archive` for direct server access scenarios.

**Next Steps**: Evaluate specific migration requirements and choose appropriate toolchain based on access level and technical capabilities.