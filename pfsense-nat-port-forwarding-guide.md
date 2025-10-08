# pfSense NAT Port Forwarding Guide

## Opening TCP Port 3389 (RDP) in pfSense

### Configuration Steps

1. **Navigate to:** Firewall → NAT → Port Forward
2. **Click:** Add (↑) to create new rule

### Required Settings

**Basic Configuration:**
- **Interface:** WAN
- **Protocol:** TCP
- **Source:** Any (or restrict to specific IPs for security)

**Destination Configuration:**
- **Destination:** WAN Address
- **Destination port range:** 
  - **From:** `3389`
  - **To:** `3389`

**Redirect Target Configuration:**
- **Redirect Target IP:** `[Internal device IP]` (e.g., `192.168.1.100`)
- **Redirect Target Port:** `3389`
- **Description:** "RDP Access" or similar

### Security Considerations

- Consider changing the external port (e.g., `33389` → `3389`) for security
- Restrict source IPs when possible
- Enable logging for monitoring access attempts

### Post-Configuration

1. **Save** the NAT rule
2. **Create firewall rule** (pfSense will prompt automatically)
3. **Apply Changes**
4. **Test** connectivity from external network

### Common Port Forward Examples

| Service | External Port | Internal IP | Internal Port | Protocol |
|---------|---------------|-------------|---------------|----------|
| RDP     | 3389          | 192.168.1.100 | 3389        | TCP      |
| SSH     | 22            | 192.168.1.101 | 22          | TCP      |
| HTTP    | 80            | 192.168.1.102 | 80          | TCP      |
| HTTPS   | 443           | 192.168.1.102 | 443         | TCP      |

### Troubleshooting

- Check firewall logs: Status → System Logs → Firewall
- Verify internal device is accessible from pfSense
- Confirm no conflicting rules exist
- Test from external network, not internal (hairpin NAT issues)

### Key Points

- **Destination port range** = External port accessible from internet
- **Redirect Target** = Internal device and port to forward traffic to
- Both firewall NAT rule AND firewall rule are required
- Changes require "Apply Changes" to take effect

## CLI Method: Interactive Script

### Quick Setup with SSH Script

For faster port forwarding setup via SSH, use the interactive script:

1. **Download the script** to your pfSense system:
   ```bash
   curl -O https://your-server/pfsense-port-forward-interactive.sh
   chmod +x pfsense-port-forward-interactive.sh
   ```

2. **Run the script** as root/admin:
   ```bash
   ./pfsense-port-forward-interactive.sh
   ```

### Script Features

- **Interactive Protocol Selection**: Choose TCP, UDP, or TCP/UDP with arrow keys
- **Automatic IP Discovery**: Scans DHCP leases, ARP table, and static assignments
- **Arrow Key Navigation**: Browse available IPs with up/down arrows
- **Safety Features**: Auto-backup config.xml before changes
- **Validation**: Port number and IP address validation
- **Auto-reload**: Automatically reloads pfSense configuration

### Script Usage Flow

1. **Protocol Selection**: Use arrow keys to select TCP/UDP/TCP+UDP
2. **Port Configuration**: Enter external and internal port numbers
3. **IP Selection**: Browse and select target IP from discovered devices
4. **Confirmation**: Review settings and confirm creation
5. **Auto-Apply**: Script creates rule and reloads configuration

### CLI Commands for Manual Setup

For direct command-line configuration without the script:

```bash
# View DHCP leases
cat /var/dhcpd/var/db/dhcpd.leases

# View ARP table
arp -a

# Backup config
cp /conf/config.xml /conf/backup/config.xml.backup.$(date +%Y%m%d_%H%M%S)

# Reload configuration
echo "configsync;reloadcfg" | pfSsh.php -q
```

### Script Location

The interactive script is available at:
`/home/user1/shawndev1/helpful_memory_and_test_files/pfsense-port-forward-interactive.sh`

### Security Notes for CLI Method

- Script creates automatic config backups before changes
- Includes port validation and IP address verification
- Generates unique tracker IDs for proper rule identification
- Automatically creates descriptive rule names
- Requires root/admin access on pfSense system