# Runtipi Architecture & Configuration Guide

## Overview

Runtipi is a homeserver management platform that simplifies self-hosting applications through a web interface. This documentation covers the technical architecture, Traefik integration, and customization options based on analysis of a live Runtipi v4.3.0 installation.

## Core Architecture

### Technology Stack
- **Frontend**: React with TypeScript
- **Backend**: NestJS (Node.js framework)
- **Database**: PostgreSQL 14
- **Message Queue**: RabbitMQ 4-alpine
- **Reverse Proxy**: Traefik v3.2
- **Container Engine**: Docker with Docker Compose
- **ORM**: Drizzle-ORM

### Main Components

#### 1. Runtipi Core Service (`runtipi`)
- **Image**: `ghcr.io/runtipi/runtipi:${TIPI_VERSION}`
- **Port**: 3000 (internal)
- **Health Check**: `curl -f http://localhost:3000/api/health`
- **Purpose**: Main application server providing web UI and API

#### 2. Reverse Proxy (`runtipi-reverse-proxy`)
- **Image**: `traefik:v3.2`
- **Ports**: 80 (HTTP), 443 (HTTPS)
- **Purpose**: Routes traffic to applications and handles SSL termination

#### 3. Database (`runtipi-db`)
- **Image**: `postgres:14`
- **Database**: `tipi`
- **User**: `tipi`
- **Purpose**: Stores application metadata, user data, and configurations

#### 4. Message Queue (`runtipi-queue`)
- **Image**: `rabbitmq:4-alpine`
- **Port**: 5672
- **User**: `tipi`
- **Purpose**: Handles background tasks and async operations

## Directory Structure

```
/home/user1/runtipi/
├── VERSION                 # Current version (v4.3.0)
├── docker-compose.yml      # Main orchestration file
├── .env                    # Environment variables
├── apps/                   # Installed applications
│   └── migrated/           # Migrated app instances
├── app-data/               # Application data and configurations
│   └── migrated/           # App-specific data directories
├── repos/                  # App store repositories
│   ├── 29ca930b.../        # Main app store repo
│   ├── custom-store/       # Custom app store
│   └── migrated/           # Legacy app store
├── state/                  # System state and settings
│   ├── settings.json       # Main configuration
│   └── seed                # Initial setup data
├── traefik/                # Traefik configuration
│   ├── traefik.yml         # Main Traefik config
│   ├── dynamic/            # Dynamic configuration
│   ├── shared/             # Shared resources (acme.json)
│   └── tls/                # TLS certificates
├── user-config/            # User customizations
│   ├── tipi-compose.yml    # Global Docker Compose overrides
│   └── migrated/           # Per-app customizations
├── media/                  # Media storage for apps
├── logs/                   # Application logs
├── backups/                # Application backups
└── cache/                  # Application cache
```

## Traefik Integration

### Configuration Structure

Traefik is configured through multiple layers:

1. **Static Configuration** (`traefik/traefik.yml`)
2. **Dynamic Configuration** (`traefik/dynamic/`)
3. **Docker Labels** (automatically generated)

### Static Configuration (`traefik/traefik.yml`)
```yaml
api:
  dashboard: true
  insecure: true

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    watch: true
    exposedByDefault: false
  file:
    directory: /etc/traefik/dynamic
    watch: true

entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"
    http:
      tls:
        certResolver: myresolver

certificatesResolvers:
  myresolver:
    acme:
      email: shawn@partsfortechs.com
      storage: /shared/acme.json
      dnsChallenge:
        provider: cloudflare
        delayBeforeCheck: 0

log:
  level: ERROR
```

### Automatic Label Generation

Runtipi automatically generates Traefik labels for applications. Example from Portainer:

```yaml
labels:
  traefik.enable: true
  traefik.docker.network: runtipi_tipi_main_network
  traefik.http.middlewares.portainer-migrated-web-redirect.redirectscheme.scheme: https
  traefik.http.services.portainer-migrated.loadbalancer.server.port: "9000"
  traefik.http.routers.portainer-migrated-local-insecure.rule: Host(`portainer-migrated.${LOCAL_DOMAIN}`)
  traefik.http.routers.portainer-migrated-local-insecure.entrypoints: web
  traefik.http.routers.portainer-migrated-local-insecure.service: portainer-migrated
  traefik.http.routers.portainer-migrated-local-insecure.middlewares: portainer-migrated-web-redirect
  traefik.http.routers.portainer-migrated-local.rule: Host(`portainer-migrated.${LOCAL_DOMAIN}`)
  traefik.http.routers.portainer-migrated-local.entrypoints: websecure
  traefik.http.routers.portainer-migrated-local.service: portainer-migrated
  traefik.http.routers.portainer-migrated-local.tls: true
  runtipi.managed: true
  runtipi.appurn: portainer:migrated
```

### Label Pattern Analysis

Each app gets:
- **Service Definition**: `traefik.http.services.{app-name}.loadbalancer.server.port`
- **HTTP Router**: Routes HTTP traffic and redirects to HTTPS
- **HTTPS Router**: Handles secure traffic with TLS
- **Middleware**: Handles redirects and authentication
- **Network**: Connects to `runtipi_tipi_main_network`

## App Management System

### App Configuration Schema

Apps are configured through two main files:

1. **`config.json`** - App metadata and UI configuration
2. **`docker-compose.json`** - Dynamic compose configuration (v3.2+)

### App Configuration (`config.json`)
```json
{
  "$schema": "../app-info-schema.json",
  "name": "Portainer",
  "port": 9443,
  "available": true,
  "exposable": true,
  "dynamic_config": true,
  "id": "portainer",
  "tipi_version": 45,
  "version": "2.31.3",
  "categories": ["utilities"],
  "description": "Container management platform",
  "short_desc": "Making Docker and Kubernetes management easy.",
  "author": "portainer",
  "source": "https://github.com/portainer/portainer",
  "website": "https://www.portainer.io",
  "form_fields": [],
  "supported_architectures": ["arm64", "amd64"],
  "created_at": 1691943801422,
  "updated_at": 1752088434279
}
```

### Dynamic Compose Configuration (`docker-compose.json`)
```json
{
  "$schema": "../dynamic-compose-schema.json",
  "services": [
    {
      "name": "portainer",
      "image": "portainer/portainer-ce:2.31.3-alpine",
      "isMain": true,
      "internalPort": 9000,
      "volumes": [
        {
          "hostPath": "/var/run/docker.sock",
          "containerPath": "/var/run/docker.sock"
        },
        {
          "hostPath": "${APP_DATA_DIR}/data",
          "containerPath": "/data"
        }
      ]
    }
  ]
}
```

### Dynamic Compose Features

The dynamic compose system supports:
- **Service Definition**: Name, image, and basic container settings
- **Port Configuration**: `internalPort` for the main service port
- **Volume Mounts**: Host path to container path mappings
- **Environment Variables**: Service-specific environment configuration
- **Health Checks**: Container health monitoring
- **Dependencies**: Service startup order
- **Resource Limits**: CPU and memory constraints
- **Additional Ports**: TCP/UDP port mappings
- **Networking**: Custom network configurations

## Custom Configuration Options

### 1. Global Docker Compose Overrides (`user-config/tipi-compose.yml`)

This file allows global modifications to the main Docker Compose configuration:

```yaml
services:
  runtipi-reverse-proxy:
    ports:
      - 8080:8080  # Expose Traefik dashboard
    environment:
      - CF_DNS_API_TOKEN=your-cloudflare-token
```

**Key Points:**
- Modifies the main Runtipi services
- Persists across updates
- Useful for exposing additional ports or adding environment variables

### 2. Per-App Customizations (`user-config/{app-name}/`)

Create app-specific overrides:

```
user-config/
└── migrated/
    └── matrix-conduit/
        └── docker-compose.yml
```

**Features:**
- Override default app configurations
- Add custom environment variables via `app.env`
- Mount additional volumes
- Modify container settings

### 3. Traefik Configuration Persistence

Enable persistent Traefik configuration:

```json
{
  "persistTraefikConfig": true
}
```

Set in `state/settings.json` to prevent Traefik config overwrites.

### 4. Settings Configuration (`state/settings.json`)

Current installation settings:
```json
{
  "allowErrorMonitoring": false,
  "internalIp": "192.168.1.107",
  "appsRepoUrl": "https://github.com/runtipi/runtipi-appstore",
  "domain": "runtipi1.asapllc.com",
  "appDataPath": "/home/user1/runtipi",
  "localDomain": "tipi.local",
  "guestDashboard": false,
  "allowAutoThemes": true,
  "persistTraefikConfig": true,
  "port": 80,
  "sslPort": 443,
  "listenIp": "192.168.1.107",
  "timeZone": "America/New_York",
  "eventsTimeout": 5,
  "advancedSettings": false,
  "forwardAuthUrl": "http://runtipi:3000/api/auth/traefik",
  "logLevel": "info"
}
```

## Network Architecture

### Container Networks

1. **`runtipi_tipi_main_network`** (Bridge)
   - Main network for all Runtipi services
   - Shared by core services and apps
   - Enables service discovery

2. **App-Specific Networks**
   - Each app gets its own network (e.g., `portainer_migrated_network`)
   - Isolated from other apps
   - Connected to main network for proxy access

### Service Discovery

- Traefik uses Docker provider for automatic service discovery
- Services are discovered via Docker labels
- No manual route configuration required

## SSL/TLS Configuration

### Certificate Management
- **Let's Encrypt**: Automatic certificate generation
- **DNS Challenge**: Uses Cloudflare DNS for validation
- **Storage**: Certificates stored in `traefik/shared/acme.json`

### Certificate Resolver Configuration
```yaml
certificatesResolvers:
  myresolver:
    acme:
      email: shawn@partsfortechs.com
      storage: /shared/acme.json
      dnsChallenge:
        provider: cloudflare
        delayBeforeCheck: 0
```

## Authentication & Authorization

### Forward Authentication
- **Middleware**: `runtipi.forwardauth.address`
- **Endpoint**: `http://runtipi:3000/api/auth/traefik`
- **Purpose**: Centralized authentication for all apps

### Authentication Flow
1. User accesses app URL
2. Traefik intercepts request
3. Forward auth middleware validates session
4. Valid requests proceed to app
5. Invalid requests redirect to login

## App Store System

### Repository Structure
```
repos/
├── 29ca930b.../          # Main official app store
│   ├── apps/             # App definitions
│   ├── package.json      # Node.js dependencies
│   └── schemas/          # JSON schemas
├── custom-store/         # Custom app repository
└── migrated/            # Legacy app store
```

### App Store Configuration
- **Main Store**: `https://github.com/runtipi/runtipi-appstore`
- **Custom Stores**: Additional repositories can be added
- **Schemas**: JSON schemas validate app configurations

## Data Flow & Lifecycle

### App Installation Process
1. User selects app from store
2. Runtipi downloads app configuration
3. Environment variables are generated
4. Docker Compose file is created
5. Traefik labels are applied
6. Container is deployed
7. Health checks verify deployment

### App Update Process
1. New version detected in app store
2. Runtipi pulls updated configuration
3. Container is recreated with new image
4. Data volumes are preserved
5. Traefik routes are updated

### Backup & Migration
- **App Data**: Stored in `app-data/` directory
- **Backups**: Automated backups in `backups/` directory
- **Migration**: Apps can be migrated between installations

## Security Considerations

### Container Security
- **Isolation**: Each app runs in its own container
- **Networks**: App-specific networks prevent cross-app communication
- **Volumes**: Data volumes are isolated per app

### Access Control
- **Forward Authentication**: Centralized login system
- **SSL/TLS**: All traffic encrypted in transit
- **Internal Networks**: Services not directly exposed to internet

### Configuration Security
- **Environment Variables**: Sensitive data in environment files
- **File Permissions**: Proper file system permissions
- **Docker Socket**: Controlled access to Docker daemon

## Troubleshooting & Maintenance

### Common Issues
- **Port Conflicts**: Check app port assignments
- **SSL Issues**: Verify DNS settings for Let's Encrypt
- **Container Failures**: Check logs in `logs/` directory
- **Network Issues**: Verify Docker network configuration

### Maintenance Tasks
- **Updates**: Regular Runtipi version updates
- **Backups**: Regular backup of app data
- **Monitoring**: Check logs and health status
- **Cleanup**: Remove unused containers and images

## External Integrations

### Cloudflare Tunnels
- **Purpose**: Expose apps without port forwarding
- **Configuration**: Via Cloudflare dashboard
- **Benefits**: IP hiding, DDoS protection, no firewall changes

### DNS Integration
- **Cloudflare DNS**: For Let's Encrypt challenges
- **Local DNS**: `.local` domain for internal access
- **Dynamic DNS**: Automatic IP updates

## CLI Management

### Runtipi CLI (`runtipi-cli`)
- **Location**: `/home/user1/runtipi/runtipi-cli`
- **Functions**: App management, updates, maintenance
- **Usage**: `./runtipi-cli app start/stop/restart [appname]`

This comprehensive documentation provides the technical foundation for understanding and customizing Runtipi installations. The modular architecture and configuration options make it highly adaptable for various homeserver requirements.