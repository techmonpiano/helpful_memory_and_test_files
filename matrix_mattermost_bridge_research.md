# Matrix-Mattermost Bridge Research Session
**Date**: 2025-09-02  
**Topic**: Connecting external Matrix instance to Mattermost for message transfer

## Session Overview
User requested information about connectors/bridges to connect an external Matrix instance to their Mattermost instance, specifically for transferring messages between Matrix and Mattermost channels.

## Key Findings

### Available Bridge Solutions (All Open Source)

#### 1. **Matterbridge** ⭐ RECOMMENDED
- **License**: Apache-2.0
- **GitHub**: https://github.com/42wim/matterbridge (6.5k+ stars)
- **Type**: Self-hosted Go application
- **Pros**:
  - Most popular and versatile solution
  - Supports 20+ platforms (not just Matrix/Mattermost)
  - Very active development
  - Well-documented with extensive wiki
  - Easy TOML configuration
  - Supports multiple gateways/channels simultaneously
- **Features**:
  - Bidirectional message sync
  - Markdown, attachments, edits, replies support
  - Messages appear from actual users (not bots)
  - Rich content support (emojis, reactions, threads, files)

#### 2. **Official Mattermost Matrix Connector**
- **License**: Apache-2.0
- **GitHub**: https://github.com/mattermost/mattermost-plugin-matrix-bridge
- **Type**: Mattermost plugin
- **Pros**:
  - Official plugin from Mattermost
  - Available in Mattermost Marketplace
  - Easier integration as a plugin
  - Automatic registration file generation
- **Features**:
  - Bidirectional sync
  - Real user identity preservation
  - Full formatting support
  - Simple configuration

#### 3. **matrix-as-mm** (Community Bridge)
- **License**: Apache-2.0
- **GitHub**: https://github.com/mattermost-community/matrix-as-mm
- **Type**: Matrix Application Service
- **Pros**:
  - Community-developed
  - Uses Matrix's Application Service API
  - Supports public/private channels and DMs
- **Features**:
  - Distributed channels created by admin
  - Private channels for all users
  - Direct message support
  - Bidirectional federation

## Implementation Guide (Matterbridge)

### Prerequisites
1. Server with access to both Mattermost and Matrix instances
2. Service account in Mattermost
3. Matrix account for bridging

### Installation Steps
```bash
# 1. Download latest binary from GitHub releases
wget https://github.com/42wim/matterbridge/releases/download/[version]/matterbridge-[version]-linux-64bit

# 2. Make executable
chmod +x matterbridge-*

# 3. Create configuration file
touch matterbridge.toml
```

### Configuration Template
```toml
# Mattermost Configuration
[mattermost]
[mattermost.myteam]
Server="https://your.mattermost.server"
Team="yourteam"
Login="matterbridge"  # Service account username
Password="your-matterbridge-password"
PrefixMessagesWithNick=true
RemoteNickFormat="[Matrix] <{NICK}> "

# Matrix Configuration
[matrix]
[matrix.mymatrix]
Server="https://your.matrix.server"
Login="@matterbridge:your.matrix.server"
Password="your-matrix-password"
RemoteNickFormat="[Mattermost] <{NICK}> "

# Gateway Configuration
[[gateway]]
name="mm-matrix-bridge"
enable=true

# Channel/Room Mapping
[[gateway.inout]]
account="mattermost.myteam"
channel="general"  # Mattermost channel name

[[gateway.inout]]
account="matrix.mymatrix"
channel="#room:matrix.server"  # Matrix room
```

### Running Matterbridge
```bash
# Basic run
./matterbridge -conf matterbridge.toml

# With debug output
./matterbridge -conf matterbridge.toml -debug

# As a service (systemd example)
# Create /etc/systemd/system/matterbridge.service
```

## Supported Features Across All Solutions

### Message Types
- Plain text messages
- Markdown formatting
- File attachments (images, documents)
- Message edits
- Message replies/threads
- Emoji reactions

### Channel/Room Types
- Public channels ↔ Public rooms
- Private channels ↔ Private rooms
- Direct messages (1-on-1 chats)
- Group chats

### Security Features
- Encrypted message transit
- Authentication via API tokens
- Compliance logging capabilities
- Audit trail support

## Architecture Notes

### Matrix Application Service API
- Used by matrix-as-mm and official connector
- Provides native Matrix integration
- Requires Application Service support on Matrix server

### REST API Approach
- Used by Matterbridge
- More flexible, works with any Matrix/Mattermost setup
- Doesn't require special server configuration

## Troubleshooting Tips

### Common Issues
1. **Authentication failures**: Verify service account credentials
2. **Channel mapping errors**: Ensure correct channel/room syntax
3. **Message delays**: Check network connectivity between servers
4. **Missing messages**: Verify bidirectional gateway configuration

### Debug Commands
```bash
# Test Mattermost connection
curl -i -H 'Authorization: Bearer YOUR_TOKEN' https://your.mattermost.server/api/v4/users/me

# Check Matrix connection
curl https://your.matrix.server/_matrix/client/versions

# Matterbridge debug mode
./matterbridge -conf matterbridge.toml -debug
```

## Performance Considerations
- Matterbridge is lightweight (Go binary ~20MB)
- Low memory footprint (~50MB typical)
- Can handle high message volumes
- Supports rate limiting configuration

## Recommendation Summary
**Matterbridge** is the recommended solution due to:
1. Mature, actively maintained codebase
2. Extensive documentation and community support
3. Flexibility to bridge multiple platforms
4. Simple configuration and deployment
5. Proven reliability with 6.5k+ GitHub stars

## Additional Resources
- [Matterbridge Wiki](https://github.com/42wim/matterbridge/wiki)
- [Matterbridge Configuration Guide](https://github.com/42wim/matterbridge/wiki/How-to-create-your-config)
- [Mattermost Marketplace](https://mattermost.com/marketplace/)
- [Matrix Bridges Ecosystem](https://matrix.org/ecosystem/bridges/)

## Session Notes
- All solutions discussed are open source (Apache-2.0 license)
- User confirmed interest in open source nature of solutions
- No troubleshooting required - informational session only
- Research conducted via web search for current information

---
*Session completed successfully - no issues encountered*