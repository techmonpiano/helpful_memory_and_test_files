# Memory Bank: Perplexica + Ollama + Cloudflare Setup - June 2025

**Session Date:** June 25, 2025  
**Project:** Independent Ollama Service with Perplexica and Cloudflare Tunnel Integration  
**Status:** ✅ Complete Implementation

## 🎯 Project Overview

Created a comprehensive Docker-based setup with two independent services:
1. **Shared Ollama Service** - Independent container with phi4-reasoning models
2. **Perplexica with Cloudflare** - AI search engine with secure remote access

## 🏗️ Architecture Implemented

### **Key Design Decisions:**
- **External Docker Network** (`ollama-shared-network`) for cross-project sharing
- **Separate Cloudflare Tunnels** for different services (optional)
- **Microsoft Phi-4 Models** as primary reasoning models (14B + 3.8B variants)
- **Security-first approach** with Cloudflare Access authentication

### **Directory Structure:**
```
/home/user1/shawndev1/
├── ollama-shared/                    # Independent Ollama service
│   ├── docker-compose.yml           # Base configuration + GPU support
│   ├── docker-compose.tunnel.yml    # Optional Cloudflare tunnel
│   ├── entrypoint.sh                # Auto-downloads phi4 models
│   ├── setup-ollama.sh              # Interactive setup script
│   ├── .env.example                 # Configuration template
│   └── README.md                     # Comprehensive documentation
│
├── perplexity-docker/               # Perplexica with tunnel support
│   ├── docker-compose.yml           # Updated to use external network
│   ├── docker-compose.tunnel.yml    # Cloudflare tunnel for web GUI
│   ├── setup-perplexica.sh          # Enhanced setup script
│   ├── setup.sh                     # Original script (preserved)
│   └── .env.example                 # Updated with Cloudflare options
│
└── CLOUDFLARE_SETUP.md             # Complete tunnel setup guide
```

## 🔬 Research Findings

### **AI Model Selection Process:**
1. **Initial Question:** Which open source reasoning models are best (non-Chinese)?
2. **Research Results:**
   - **Microsoft Phi-4 Reasoning** (14B) - Best mathematical reasoning (MATH: 80.4, GPQA: 56.1)
   - **Mistral Magistral Small** - Good enterprise/compliance features
   - **Meta Llama 3.3 70B** - Balanced performance but larger

3. **Final Choice:** Microsoft Phi-4 for superior reasoning performance in smaller package

### **Anthropic Integration Research:**
- **Finding:** Perplexica only supports Anthropic via API (pay-per-token)
- **Not supported:** Claude Pro/Max subscription plans ($20-200/month)
- **Reason:** Separate billing systems - subscriptions ≠ API access

### **Remote Access Solutions Evaluated:**
1. **Cloudflare Tunnel** ✅ CHOSEN - Zero port forwarding, built-in SSL, free tier
2. **Tailscale VPN** - Most secure but more complex for team access
3. **Direct Nginx Proxy** - Requires manual SSL/auth setup

## 🛠️ Technical Implementation Details

### **Ollama Service Features:**
- **Auto-model download:** phi4-reasoning + phi4-mini-reasoning
- **GPU acceleration:** NVIDIA support with health checks
- **Performance tuning:** 4 parallel processes, 24h keep-alive
- **External network:** `ollama-shared-network` for project sharing
- **Health monitoring:** API version endpoint checks

### **Perplexica Enhancements:**
- **Network integration:** Connects to `shared-ollama:11434`
- **Cloudflare tunnel:** Secure remote access to web GUI
- **Dependency checking:** Verifies Ollama service before starting
- **Multiple AI backends:** OpenAI, Groq, Anthropic, shared Ollama

### **Security Implementation:**
- **No direct port exposure** - all access via Cloudflare tunnels
- **Authentication ready** - Cloudflare Access integration documented
- **Network isolation** - Docker external networks for service separation
- **API security warnings** - Ollama has no built-in auth (documented)

## 📋 Setup Scripts Created

### **ollama-shared/setup-ollama.sh:**
- Docker/GPU validation
- External network creation
- Optional Cloudflare tunnel configuration
- Model download monitoring
- Service health verification

### **perplexity-docker/setup-perplexica.sh:**
- Ollama dependency checking
- AI model configuration (OpenAI, Groq, Anthropic, Ollama)
- Cloudflare tunnel setup for web GUI
- Port conflict detection
- Browser auto-opening

## 🌐 Cloudflare Tunnel Configuration

### **Two Tunnel Types Implemented:**

**1. Perplexica Web GUI (Primary):**
- **Purpose:** Remote access to AI search interface
- **URL Pattern:** `perplexica.your-domain.com`
- **Service Target:** `perplexica-app:3000`
- **Authentication:** Cloudflare Access (email, Google, GitHub SSO)

**2. Ollama API (Optional):**
- **Purpose:** Direct API access for external projects
- **URL Pattern:** `ollama.your-domain.com`
- **Service Target:** `shared-ollama:11434`
- **Security:** API key recommended via Cloudflare Access

### **Setup Process:**
1. Cloudflare Zero Trust tunnel creation
2. Public hostname configuration
3. Tunnel token integration in .env files
4. Cloudflare Access policy setup
5. Service-specific authentication rules

## 🚀 Deployment Commands

### **Quick Start Sequence:**
```bash
# 1. Setup shared Ollama (downloads ~11GB of models)
cd ollama-shared
./setup-ollama.sh

# 2. Setup Perplexica with remote access
cd ../perplexity-docker
./setup-perplexica.sh
```

### **Advanced Commands:**
```bash
# Start with tunnels manually
docker compose -f docker-compose.yml -f docker-compose.tunnel.yml up -d

# Check tunnel status
docker logs perplexica-tunnel
docker logs ollama-tunnel

# Monitor model downloads
docker logs shared-ollama -f
```

## 📊 Performance Characteristics

### **Phi-4 Model Performance:**
- **phi4-reasoning (14B):** ~11GB disk, 16GB+ RAM recommended
- **phi4-mini-reasoning (3.8B):** ~3.2GB disk, 4GB+ RAM minimum
- **Download time:** 10-15 minutes on good connection
- **GPU acceleration:** Requires nvidia-container-toolkit

### **Resource Usage:**
- **Ollama container:** Base 2GB + models
- **Perplexica:** ~1GB for app + SearxNG
- **Network overhead:** Minimal with external networks
- **Shared benefits:** Single model download serves all projects

## 🔒 Security Best Practices Implemented

### **Network Security:**
- External Docker networks for isolation
- No public port exposure by default
- Cloudflare tunnels with encryption

### **Authentication:**
- Cloudflare Access for user management
- Support for multiple auth providers
- Team access control documentation

### **API Security:**
- Warning about Ollama's lack of built-in auth
- Recommendations for proxy-based auth
- Cloudflare Access as authentication layer

## 🔧 Troubleshooting Solutions

### **Common Issues Documented:**
1. **GPU not detected:** nvidia-container-toolkit installation
2. **Network connectivity:** External network verification
3. **Tunnel connection:** Token validation and logs
4. **Model download slow:** Internet connection and disk space
5. **Port conflicts:** Automatic detection and guidance

### **Debug Commands:**
```bash
# Service health
docker compose ps
docker network inspect ollama-shared-network

# Model availability
docker exec shared-ollama ollama list

# API connectivity
curl http://localhost:11434/api/version
```

## 🎯 Project Benefits Achieved

### **For Current Setup:**
✅ **Single Ollama instance** serves multiple projects  
✅ **Phi-4 reasoning models** provide superior AI capabilities  
✅ **Secure remote access** from any device/location  
✅ **Team collaboration** via Cloudflare Access  
✅ **Resource efficiency** - no duplicate containers/models  

### **For Future Expansion:**
✅ **Scalable architecture** - easy to add new AI projects  
✅ **Model sharing** - any project can use phi4 models  
✅ **Network foundation** - external networks for service discovery  
✅ **Documentation complete** - setup guides and troubleshooting  

## 🔮 Future Enhancement Opportunities

### **Immediate:**
- Add more AI models (Llama 3.3, Mistral, etc.)
- Implement Nginx proxy with custom auth
- Add monitoring dashboard (Grafana/Prometheus)

### **Advanced:**
- Load balancing across multiple Ollama instances
- Model caching optimization
- Automated backup and restore
- CI/CD pipeline for model updates

## 📝 Configuration Templates

### **Key Environment Variables:**
```bash
# Ollama Configuration
OLLAMA_API_URL=http://shared-ollama:11434
OLLAMA_HOST=0.0.0.0:11434
OLLAMA_KEEP_ALIVE=24h

# Cloudflare Tunnels
CLOUDFLARE_TUNNEL_TOKEN=eyJhIjoiY...
ENABLE_REMOTE_ACCESS=true
ENABLE_OLLAMA_TUNNEL=false

# AI Model APIs
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk-...
ANTHROPIC_API_KEY=...
```

### **Docker Network Commands:**
```bash
# Create shared network
docker network create ollama-shared-network

# Connect existing container
docker network connect ollama-shared-network container-name

# Inspect network
docker network inspect ollama-shared-network
```

## 🎓 Key Learnings

### **Technical:**
1. **External Docker networks** enable true service sharing
2. **Cloudflare tunnels** eliminate port forwarding complexity
3. **Microsoft Phi-4** offers excellent reasoning in small package
4. **Automated setup scripts** critical for complex multi-service deployments

### **Security:**
1. **Never expose Ollama directly** to internet without auth
2. **Cloudflare Access** provides enterprise-grade authentication
3. **Network isolation** important even with trusted services
4. **Documentation critical** for team adoption

### **Performance:**
1. **Model sharing** dramatically reduces resource usage
2. **GPU acceleration** essential for larger models
3. **Keep-alive settings** prevent model reload delays
4. **Health checks** ensure service reliability

## 🔗 Related Documentation

- **CLOUDFLARE_SETUP.md** - Complete tunnel configuration
- **ollama-shared/README.md** - Ollama service documentation  
- **perplexity-docker/README.md** - Perplexica setup guide
- **.env.example files** - Configuration templates

## 💡 Session Notes

### **User Requirements Evolution:**
1. Started with basic Perplexica Docker setup
2. Added Microsoft Phi-4 model preference
3. Requested independent Ollama container for project sharing
4. Added Cloudflare tunnel requirement for remote access
5. Specified separate tunnels for GUI vs API access

### **Implementation Approach:**
- Researched best practices before implementation
- Created modular, reusable components
- Prioritized security and documentation
- Built with future expansion in mind
- Comprehensive testing and troubleshooting guides

## ✅ Completion Status

**All requested features implemented:**
- ✅ Independent Ollama container with phi4-reasoning
- ✅ Perplexica web GUI with Cloudflare tunnel
- ✅ Optional Ollama API tunnel for external projects
- ✅ Comprehensive documentation and setup scripts
- ✅ Security-first approach with authentication options
- ✅ Resource-efficient design for multiple project sharing

**Ready for production deployment and team use.**

---

*This memory bank captures the complete session for future reference and enhancement.*