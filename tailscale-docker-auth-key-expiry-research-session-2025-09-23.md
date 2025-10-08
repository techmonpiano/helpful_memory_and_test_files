# Tailscale Docker Container Auth Key Expiry Research Session - 2025-09-23

## Session Summary
Research session focused on understanding Tailscale auth key expiry limitations for Docker containers and finding workarounds to avoid the 90-day re-authentication requirement.

## User Question
When creating Tailscale auth keys, the maximum duration is 90 days. If a machine is marked as "no key expiry" after authentication, will it continue working beyond 90 days? Are there workarounds for permanent authentication?

## Key Findings

### 1. Auth Keys vs Node Keys (Critical Distinction)
- **Auth keys**: Used for initial authentication (90-day max limit)
- **Node keys**: Assigned after authentication (default 180-day expiry, but can be disabled)
- Once authenticated, the machine operates on node keys, not the original auth key

### 2. Disable Key Expiry Feature
**Answer: YES** - Disabling key expiry after authentication will allow the container to continue working indefinitely.

**Process:**
1. Machine authenticates using 90-day auth key
2. Admin console → Machines page → Find device → Menu → "Disable Key Expiry"
3. Machine will no longer require periodic re-authentication

### 3. Better Solutions for Docker Containers

#### Option 1: Tagged Auth Keys (Automatic)
- Create auth keys with tags in ACL
- Tagged devices automatically have key expiry disabled
- No manual intervention required

#### Option 2: OAuth Client Secrets (Recommended)
- OAuth secrets never expire
- Use directly as `TS_AUTHKEY` environment variable
- Generate in admin console: Settings → OAuth clients
- Best solution for automated deployments

#### Option 3: Persistent Storage
- Use Docker volumes to persist Tailscale state
- Once authenticated, auth key expiry doesn't matter
- State persistence allows survival of container restarts

### 4. Docker Environment Configuration
```bash
# Using OAuth client secret (recommended)
docker run -e TS_AUTHKEY=tskey-client-oauth_secret_here tailscale-container

# Using tagged auth key with persistent volume
docker run -v tailscale-data:/var/lib/tailscale -e TS_AUTHKEY=tskey-auth-tagged_key_here tailscale-container
```

## Technical Details

### Default Expiry Periods
- Auth keys: 90 days maximum
- Node keys: 180 days default (configurable 1-180 days)
- OAuth client secrets: Never expire

### Key Expiry Settings Location
- Admin console → Device Management → Key Expiry section
- Can set custom periods from 1-180 days
- Individual devices can have expiry disabled

### Clarification on "Disable Key Expiry"
- Does NOT affect data plane encryption key rotation (continues every 2 minutes per WireGuard)
- Only disables requirement for periodic SSO re-authentication
- Machine remains securely connected without manual intervention

## Recommendations

### For Production Docker Containers:
1. **Primary**: Use OAuth client secrets (never expire, fully automated)
2. **Alternative**: Use tagged auth keys (auto-disable expiry)
3. **Fallback**: Regular auth keys + manual "disable key expiry" setting

### For Development/Testing:
- Regular 90-day auth keys with manual expiry disable are sufficient
- Use persistent volumes to maintain state across container recreation

## Important Security Notes
- Disabling key expiry doesn't compromise security
- WireGuard encryption keys still rotate automatically
- Only removes the administrative overhead of periodic re-authentication
- Recommended for servers, routers, and infrastructure devices

## Session Outcome
Successfully identified multiple solutions to the 90-day auth key limitation, with OAuth client secrets being the most robust solution for automated Docker deployments. User now has clear path forward for persistent Tailscale authentication in containers.

## References
- Tailscale KB: Key expiry documentation
- Tailscale KB: Auth keys documentation
- GitHub Issues: tailscale/tailscale #1151, #7070, #4853, #4109
- Tailscale Blog: Tagged key expiry, Docker integration guide

## Tools Used
- WebSearch for official documentation and community solutions
- Multiple search queries to validate findings and explore alternatives