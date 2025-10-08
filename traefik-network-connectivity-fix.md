# Runtipi Traefik Network Connectivity Fix

## Issue Summary

**Problem**: Matrix Conduit app installed in Runtipi was not accessible externally via Cloudflare tunnel despite correct tunnel configuration pointing to `https://localhost:443`.

**Root Cause**: Docker container connected to multiple networks with incorrect gateway priorities, causing Traefik to attempt routing to an isolated network IP address that it cannot reach.

**Solution**: Reconfigure network priorities and disconnect from isolated network to force Traefik to use the main network IP.

## Technical Details

### Network Architecture Issue

Runtipi apps by default create:
1. **App-specific isolated network** (e.g., `matrix-conduit_migrated_network` - 10.128.11.0/24)
2. **Main network connection** (`runtipi_tipi_main_network` - 172.18.0.0/16)

### The Problem

With dual network configuration:
```yaml
services:
  matrix-conduit:
    networks:
      matrix-conduit_migrated_network:
        gw_priority: 0  # Higher priority - isolated network
      tipi_main_network:
        gw_priority: 1  # Lower priority - main network
```

**Result**: Docker advertises the isolated network IP (`10.128.11.2`) to Traefik, but Traefik cannot reach this network.

### Service Discovery Flow

1. **Container starts** with two network interfaces
2. **Docker service discovery** advertises the primary gateway IP to Traefik
3. **Traefik attempts to route** to `10.128.11.2:6167`
4. **Connection fails** because Traefik is only connected to the main network
5. **HTTPS requests timeout** despite successful SSL handshake

## Diagnostic Process

### Step 1: Verify Service Discovery
```bash
# Check what IP Traefik is trying to reach
docker exec runtipi-reverse-proxy wget -qO- "http://localhost:8080/api/http/services" | jq -r '.[] | select(.name | contains("matrix-conduit-migrated-conduit")) | {name: .name, loadBalancer: .loadBalancer}'
```

**Expected Output (Problem)**:
```json
{
  "name": "matrix-conduit-migrated-conduit@docker",
  "loadBalancer": {
    "servers": [
      {
        "url": "http://10.128.11.2:6167"  # <- Isolated network IP
      }
    ]
  }
}
```

### Step 2: Test Direct Connectivity
```bash
# Test if Traefik can reach the service IP
docker exec runtipi-reverse-proxy wget -qO- "http://10.128.11.2:6167/_matrix/client/versions" --timeout=5
```

**Expected Result**: Timeout - confirms network isolation

### Step 3: Verify Container Networks
```bash
# Check which networks the container is connected to
docker inspect matrix-conduit_migrated-matrix-conduit-1 | jq -r '.[0].NetworkSettings.Networks | keys'
```

**Expected Output**:
```json
[
  "matrix-conduit_migrated_matrix-conduit_migrated_network",
  "runtipi_tipi_main_network"
]
```

### Step 4: Check Main Network IP
```bash
# Verify the main network IP is accessible
docker network inspect runtipi_tipi_main_network | jq -r '.[0].Containers | to_entries[] | select(.value.Name | contains("matrix-conduit-1")) | {container: .value.Name, ip: .value.IPv4Address}'
```

**Expected Output**:
```json
{
  "container": "matrix-conduit_migrated-matrix-conduit-1",
  "ip": "172.18.0.3/16"  # <- This IP should be accessible
}
```

### Step 5: Test Main Network Connectivity
```bash
# Test if Traefik can reach the main network IP
docker exec runtipi-reverse-proxy wget -qO- "http://172.18.0.3:6167/_matrix/client/versions" --timeout=5
```

**Expected Result**: Success - confirms the fix target

## Fix Methods

### Method 1: GUI Configuration Fix (Preferred - Runtipi v4.3.0+)

**Runtipi v4.3.0+ includes the ability to edit custom user-configs directly from the web GUI.**

**Steps**:
1. **Access the app** in Runtipi web interface
2. **Navigate to Custom Config** section (or similar menu option)
3. **Edit the docker-compose.yml** directly in the GUI
4. **Make the network priority change**:
   ```yaml
   services:
     matrix-conduit:
       networks:
         matrix-conduit_migrated_network:
           gw_priority: 1    # Lower priority - isolated network
         tipi_main_network:
           gw_priority: 0    # Higher priority - Traefik can reach this
     
     matrix-conduit-well-known:
       networks:
         matrix-conduit_migrated_network:
           gw_priority: 1
         tipi_main_network:
           gw_priority: 0
   ```
5. **Save the changes** in the GUI
6. **Runtipi automatically handles** container recreation and restart

**Advantages**:
- ✅ No SSH/terminal access needed
- ✅ Changes are visible in GUI
- ✅ Automatic restart handling
- ✅ No configuration drift
- ✅ Integrated into normal workflow

### Method 2: Manual File Override (Legacy/Emergency)

**File**: `/home/user1/runtipi/user-config/migrated/matrix-conduit/docker-compose.yml`

**Only use this method if**:
- GUI method is not available
- Emergency fix needed
- GUI is not working properly

**Steps**:
1. Create user-config override:
   ```bash
   mkdir -p /home/user1/runtipi/user-config/migrated/matrix-conduit
   cp /home/user1/runtipi/apps/migrated/matrix-conduit/docker-compose.yml /home/user1/runtipi/user-config/migrated/matrix-conduit/
   ```

2. Edit the file with network priority changes (same as above)

3. Manual restart:
   ```bash
   ./runtipi-cli app stop matrix-conduit
   ./runtipi-cli app start matrix-conduit
   docker restart runtipi-reverse-proxy
   ```

**Note**: In Runtipi v4.3.0+, the GUI will pick up manual user-config overrides and display them correctly.

### Method 3: Network Isolation Fix (Alternative)

**Change in GUI or user-config file**:
```yaml
services:
  matrix-conduit:
    networks:
      tipi_main_network: {}  # Only connect to main network
  
  matrix-conduit-well-known:
    networks:
      tipi_main_network: {}  # Only connect to main network
```

### Method 4: Emergency Manual Network Disconnect

**Only use if configuration changes don't take effect**:

```bash
# Disconnect from isolated network
docker network disconnect matrix-conduit_migrated_matrix-conduit_migrated_network matrix-conduit_migrated-matrix-conduit-1

# Restart Traefik to refresh service discovery
docker restart runtipi-reverse-proxy
```

**Warning**: This is temporary - container restart will reconnect. Must implement proper config fix.

## Verification Steps

### 1. Check Service Discovery
```bash
docker exec runtipi-reverse-proxy wget -qO- "http://localhost:8080/api/http/services" | jq -r '.[] | select(.name | contains("matrix-conduit-migrated-conduit")) | {name: .name, loadBalancer: .loadBalancer}'
```

**Expected Output (Fixed)**:
```json
{
  "name": "matrix-conduit-migrated-conduit@docker",
  "loadBalancer": {
    "servers": [
      {
        "url": "http://172.18.0.3:6167"  # <- Main network IP
      }
    ]
  }
}
```

### 2. Test Local HTTPS Access
```bash
curl -s https://localhost:443/_matrix/client/versions -H "Host: hi.asapllc.com" -k --max-time 5
```

**Expected Output**:
```json
{"versions":["r0.5.0","r0.6.0","v1.1","v1.2","v1.3","v1.4","v1.5","v1.6","v1.7","v1.8","v1.9","v1.10","v1.11","v1.12"],"unstable_features":{"org.matrix.e2e_cross_signing":true,"org.matrix.msc3916.stable":true,"org.matrix.simplified_msc3575":true}}
```

### 3. Test External Access
```bash
curl -s https://hi.asapllc.com/_matrix/client/versions --max-time 10
```

**Expected Output**: Same JSON response as local test

## Step-by-Step Fix Process for Any Runtipi App

### Phase 1: Diagnosis

1. **Identify the problem**:
   ```bash
   curl -v -k https://localhost:443 -H "Host: your-app-domain.com" --max-time 5
   ```
   - If SSL handshake succeeds but then timeouts → network connectivity issue
   - If immediate connection refused → different problem

2. **Check service discovery**:
   ```bash
   docker exec runtipi-reverse-proxy wget -qO- "http://localhost:8080/api/http/services" | jq -r '.[] | select(.name | contains("your-app-name")) | {name: .name, loadBalancer: .loadBalancer}'
   ```

3. **Verify network connectivity**:
   ```bash
   # Test if Traefik can reach the advertised IP
   docker exec runtipi-reverse-proxy wget -qO- "http://ADVERTISED_IP:PORT/health-endpoint" --timeout=5
   ```

4. **Check container networks**:
   ```bash
   docker inspect your-app-container-name | jq -r '.[0].NetworkSettings.Networks | keys'
   ```

### Phase 2: Configuration Fix

#### Method A: GUI Fix (Runtipi v4.3.0+ - Preferred)

1. **Access Runtipi web interface**
2. **Navigate to your app** settings
3. **Find "Custom Config" or "Edit Docker Compose"** section
4. **Edit the network configuration** directly in the GUI:
   ```yaml
   services:
     your-main-service:
       networks:
         your-app_migrated_network:
           gw_priority: 1    # Lower priority
         tipi_main_network:
           gw_priority: 0    # Higher priority - Traefik accessible
   ```
5. **Save the changes** - Runtipi will automatically restart the app

#### Method B: Manual Override (Legacy/Emergency)

1. **Create user-config override**:
   ```bash
   mkdir -p /home/user1/runtipi/user-config/migrated/your-app-name
   cp /home/user1/runtipi/apps/migrated/your-app-name/docker-compose.yml /home/user1/runtipi/user-config/migrated/your-app-name/
   ```

2. **Edit network configuration** (same as above)

3. **Restart application**:
   ```bash
   ./runtipi-cli app stop your-app-name
   ./runtipi-cli app start your-app-name
   docker restart runtipi-reverse-proxy
   ```

### Phase 3: Emergency Fix (if config doesn't work)

1. **Manually disconnect from isolated network**:
   ```bash
   docker network disconnect your-app_migrated_network your-app-container-name
   ```

2. **Restart Traefik**:
   ```bash
   docker restart runtipi-reverse-proxy
   ```

### Phase 4: Verification

1. **Check service discovery updated**:
   ```bash
   docker exec runtipi-reverse-proxy wget -qO- "http://localhost:8080/api/http/services" | jq -r '.[] | select(.name | contains("your-app-name"))'
   ```

2. **Test local access**:
   ```bash
   curl -s https://localhost:443/your-app-path -H "Host: your-domain.com" -k --max-time 5
   ```

3. **Test external access**:
   ```bash
   curl -s https://your-domain.com/your-app-path --max-time 10
   ```

4. **Verify GUI shows changes** (v4.3.0+):
   - Check that the custom config section shows your modifications
   - Ensures no configuration drift between GUI and reality

## Common Patterns

### Apps Most Likely to Have This Issue
- Apps with custom networking requirements
- Apps that create isolated networks for security
- Apps with multiple services (main + sidecar containers)
- Apps with database dependencies

### Network Priority Patterns
```yaml
# Correct configuration for Traefik accessibility
networks:
  app_isolated_network:
    gw_priority: 1  # Lower priority
  tipi_main_network:
    gw_priority: 0  # Higher priority - Traefik uses this
```

### IP Range Identification
- **Main network**: `172.18.0.0/16` (accessible to Traefik)
- **App networks**: `10.128.x.0/24` (isolated from Traefik)

## Troubleshooting Tips

### If GUI Configuration Doesn't Work (v4.3.0+)
1. **Check if GUI shows your changes**:
   - Navigate to custom config section
   - Verify the network priorities are displayed correctly
   - If not shown, the GUI may not have saved properly

2. **Verify app restarted**:
   ```bash
   docker ps --filter "name=your-app-name" --format "table {{.Names}}\t{{.Status}}"
   ```

3. **Check for GUI error messages**:
   - Look for error notifications in the web interface
   - Check browser console for JavaScript errors
   - Verify the save operation completed

### If Gateway Priority Doesn't Work
1. **Check if user-config override is being applied**:
   ```bash
   docker inspect container-name | jq -r '.[0].Config.Labels."com.docker.compose.project.config_files"'
   ```

2. **Verify environment variables are loaded**:
   ```bash
   docker exec container-name env | grep APP_
   ```

3. **Force container recreation**:
   ```bash
   docker rm -f container-name
   ./runtipi-cli app start app-name
   ```

### If Manual Disconnect Doesn't Persist
1. **The fix is temporary** - container restart will reconnect
2. **Must implement proper user-config override** via GUI or file
3. **Consider removing the isolated network entirely** from config

### Service Discovery Refresh
```bash
# Force Traefik to refresh service discovery
docker restart runtipi-reverse-proxy

# Alternative: restart main Runtipi container
docker restart runtipi
```

### GUI vs Manual Override Conflicts
- **In v4.3.0+**: GUI should show manual overrides correctly
- **If conflicts occur**: Use GUI to manage configuration going forward
- **Remove manual files**: If switching to GUI-only management

## Prevention

### Best Practices for New Apps
1. **Always test external connectivity** after installation
2. **Use GUI custom config** (v4.3.0+) for any network modifications
3. **Test both local and external access** endpoints
4. **Monitor Traefik service discovery** after changes
5. **Verify GUI shows changes** after making modifications

### Network Configuration Guidelines
- **Use `gw_priority: 0`** for networks that Traefik needs to access
- **Use `gw_priority: 1`** for isolated/internal networks
- **Consider if isolated networks are actually needed**
- **Document any custom network configurations**
- **Use GUI for modifications** when possible to avoid config drift

### Runtipi Version Considerations
- **v4.3.0+**: Use GUI custom config feature as primary method
- **Pre-v4.3.0**: Must use manual user-config overrides
- **Mixed environments**: GUI will display manual overrides correctly

## Related Files

- **Main app config**: `/home/user1/runtipi/apps/migrated/matrix-conduit/docker-compose.yml`
- **User override**: `/home/user1/runtipi/user-config/migrated/matrix-conduit/docker-compose.yml`
- **Environment**: `/home/user1/runtipi/app-data/migrated/matrix-conduit/app.env`
- **Traefik config**: `/home/user1/runtipi/traefik/traefik.yml`
- **Logs**: `/home/user1/runtipi/logs/app.log`

## Summary

This network connectivity issue occurs when Runtipi apps are configured with multiple networks but incorrect gateway priorities. The fix involves ensuring Traefik can reach the application containers via the main network rather than isolated networks. The solution can be implemented through configuration changes or emergency manual network disconnection.

The key insight is that Docker service discovery advertises the primary gateway IP to Traefik, so the main network (`tipi_main_network`) must have higher priority (`gw_priority: 0`) than any isolated networks.