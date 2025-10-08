# Cloudflare Tunnel Setup Guide

Complete guide for setting up secure remote access to your Perplexica and Ollama services using Cloudflare tunnels.

## 🌐 Overview

Cloudflare Tunnels provide secure, encrypted connections from your local services to the internet without:
- Opening firewall ports
- Exposing your home IP address  
- Complex VPN configurations
- Static IP requirements

## 📋 Prerequisites

1. **Cloudflare Account** (free tier works)
2. **Domain registered with Cloudflare** 
3. **Cloudflare Zero Trust setup**
4. **Running Docker services** (Ollama/Perplexica)

## 🚀 Quick Setup

### Step 1: Cloudflare Zero Trust Setup

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **Zero Trust** > **Networks** > **Tunnels**
3. Click **Create a tunnel**
4. Choose **Cloudflared** connector
5. Name your tunnel (e.g., `home-ai-services`)

### Step 2: Configure Public Hostnames

For **Perplexica Web UI**:
- **Subdomain**: `perplexica` (or your choice)
- **Domain**: `your-domain.com`
- **Service**: `HTTP`, `perplexica-app:3000`

For **Ollama API** (optional):
- **Subdomain**: `ollama` 
- **Domain**: `your-domain.com`
- **Service**: `HTTP`, `shared-ollama:11434`

### Step 3: Get Tunnel Token

1. After creating the tunnel, copy the **tunnel token**
2. It looks like: `eyJhIjoiY...` (very long string)
3. Save this token securely

## 🔧 Service Configuration

### Perplexica with Cloudflare Tunnel

1. **Copy environment file**:
   ```bash
   cd perplexity-docker
   cp .env.example .env
   ```

2. **Edit .env file**:
   ```bash
   # Cloudflare Configuration
   CLOUDFLARE_TUNNEL_TOKEN=your_tunnel_token_here
   ENABLE_REMOTE_ACCESS=true
   ```

3. **Start with tunnel**:
   ```bash
   ./setup-perplexica.sh
   # Or manually:
   docker compose -f docker-compose.yml -f docker-compose.tunnel.yml up -d
   ```

### Ollama with Optional Tunnel

1. **Edit ollama-shared/.env**:
   ```bash
   CLOUDFLARE_TUNNEL_TOKEN=your_ollama_tunnel_token_here
   ENABLE_OLLAMA_TUNNEL=true
   ```

2. **Start with tunnel**:
   ```bash
   cd ollama-shared
   ./setup-ollama.sh
   # Or manually:
   docker compose -f docker-compose.yml -f docker-compose.tunnel.yml --profile tunnel up -d
   ```

## 🔐 Cloudflare Access (Recommended)

Protect your services with authentication:

### Step 1: Create Access Application

1. Go to **Zero Trust** > **Access** > **Applications**
2. Click **Add an application** > **Self-hosted**
3. Configure:
   - **Application name**: `Perplexica AI Search`
   - **Session Duration**: `24 hours`
   - **Application domain**: `perplexica.your-domain.com`

### Step 2: Configure Authentication

Choose your preferred method:

**Email Authentication**:
- **Include**: `Emails` > `your-email@domain.com`

**Google SSO**:
- **Include**: `Login Methods` > `Google`
- Specify allowed domains or specific users

**GitHub SSO**:
- **Include**: `Login Methods` > `GitHub`
- Specify organizations or users

### Step 3: Advanced Security (Optional)

**Country Restrictions**:
- **Include**: `Country` > Select allowed countries

**IP Restrictions**:
- **Include**: `IP ranges` > Your office/home IPs

**Time-based Access**:
- **Require**: Time-based rules for business hours

## 🛠️ Troubleshooting

### Common Issues

**1. Tunnel Not Connecting**
```bash
# Check tunnel logs
docker logs perplexica-tunnel
docker logs ollama-tunnel

# Look for connection errors
grep -i error logs
```

**2. 403 Access Denied**
- Verify tunnel token is correct
- Check Cloudflare Access rules
- Ensure service URLs match exactly

**3. Service Not Accessible**
```bash
# Verify services are running
docker ps

# Check internal connectivity
docker exec perplexica-app curl http://shared-ollama:11434/api/version
```

**4. Slow Performance**
- Check if tunnel is using DERP relays
- Consider geographic proximity to Cloudflare edge
- Monitor bandwidth usage

### Debug Commands

```bash
# View all tunnel logs
docker compose logs cloudflare-tunnel-perplexica

# Test local connectivity
curl http://localhost:3000
curl http://localhost:11434/api/version

# Check network connectivity
docker network ls
docker network inspect ollama-shared-network
```

## 🔄 Management Commands

### Start Services
```bash
# Perplexica with tunnel
cd perplexity-docker
docker compose -f docker-compose.yml -f docker-compose.tunnel.yml up -d

# Ollama with tunnel
cd ollama-shared  
docker compose -f docker-compose.yml -f docker-compose.tunnel.yml --profile tunnel up -d
```

### Stop Services
```bash
docker compose down
```

### Update Tunnel Token
```bash
# Edit .env file
nano .env

# Restart tunnel service
docker compose restart cloudflare-tunnel-perplexica
```

### Monitor Status
```bash
# Service health
docker compose ps

# Tunnel status
docker logs cloudflare-tunnel-perplexica --tail=50

# Check tunnel in Cloudflare dashboard
# Zero Trust > Networks > Tunnels
```

## 🛡️ Security Best Practices

### 1. Enable Cloudflare Access
- **Always** use authentication for public services
- Regularly review access logs
- Use principle of least privilege

### 2. Monitor Usage
- Set up Cloudflare Analytics
- Monitor for unusual traffic patterns
- Enable rate limiting if needed

### 3. Regular Updates
- Keep Docker images updated
- Rotate tunnel tokens periodically
- Review access policies monthly

### 4. Network Isolation
- Use separate tunnels for different services
- Implement proper Docker network segmentation
- Don't expose admin interfaces

## 📊 Multiple Tunnel Setup

For different environments:

```yaml
# Production tunnel
CLOUDFLARE_TUNNEL_TOKEN_PROD=token_for_prod
# Staging tunnel  
CLOUDFLARE_TUNNEL_TOKEN_STAGE=token_for_stage
# Development tunnel
CLOUDFLARE_TUNNEL_TOKEN_DEV=token_for_dev
```

## 🌍 Team Access

For team environments:

1. **Create team access groups**:
   - Developers: Full access
   - QA: Limited testing access
   - Stakeholders: View-only access

2. **Configure service-specific rules**:
   - Perplexica: General team access
   - Ollama API: Developer access only

3. **Audit and logging**:
   - Enable access request logging
   - Set up alerts for unauthorized access
   - Regular access review meetings

## 📝 Configuration Examples

### Complete .env for Perplexica
```bash
# AI Models
OPENAI_API_KEY=sk-your-key-here
GROQ_API_KEY=gsk-your-key-here

# Ollama (Shared)
OLLAMA_API_URL=http://shared-ollama:11434

# Cloudflare Remote Access
CLOUDFLARE_TUNNEL_TOKEN=eyJhIjoiY...your-token-here
ENABLE_REMOTE_ACCESS=true

# Ports
PERPLEXICA_PORT=3000
SEARXNG_PORT=4000
```

### Complete .env for Ollama
```bash
# Ollama Configuration
OLLAMA_HOST=0.0.0.0:11434
OLLAMA_KEEP_ALIVE=24h

# GPU Settings
ENABLE_GPU=true
GPU_COUNT=1

# Cloudflare Tunnel (Optional)
CLOUDFLARE_TUNNEL_TOKEN=eyJhIjoiY...different-token-here
ENABLE_OLLAMA_TUNNEL=true
```

## 🎯 Access URLs

After setup, your services will be available at:

- **Perplexica**: `https://perplexica.your-domain.com`
- **Ollama API** (if enabled): `https://ollama.your-domain.com`

Authentication will be handled by Cloudflare Access if configured.

---

## 💡 Tips

- Use descriptive tunnel names for easier management
- Document your configuration for team members
- Test access from different networks/devices
- Set up monitoring alerts for tunnel health
- Consider backup tunnel tokens for redundancy

Need help? Check the Cloudflare Zero Trust documentation or create an issue in this repository.