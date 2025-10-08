# Docker Cleanup Guide and Commands

## Session Summary (July 29, 2025)

Successfully cleaned Docker system and analyzed timeshift backup for dangling resources.

### Space Reclaimed from Live System
- **Images**: ~10GB+ (removed all dangling images)
- **Volumes**: 144.2MB (removed 10 dangling volumes)
- **Build Cache**: 3.172GB (completely cleared)
- **Total Space Freed**: ~13GB+

### Timeshift Backup Analysis
- **Location**: `/run/timeshift/backup/@/var/lib/docker/`
- **Total Size**: 6.4GB
  - overlay2: 1.6GB (layer storage)
  - volumes: 4.8GB (volume data)
  - image: 6.7MB (image metadata)
- **Status**: Left unchanged (safer as backup recovery point)

## Essential Docker Cleanup Commands

### 1. Check Current Disk Usage
```bash
# Detailed breakdown of Docker disk usage
docker system df -v

# Quick summary
docker system df
```

### 2. Find Dangling Resources

#### Dangling Images
```bash
# List dangling image IDs
docker images --filter "dangling=true" -q

# List all dangling images with details
docker images --filter "dangling=true"
```

#### Dangling Volumes
```bash
# List dangling volumes
docker volume ls -f dangling=true

# List all volumes
docker volume ls
```

#### Unused Networks
```bash
# List unused networks
docker network ls --filter "dangling=true"
```

### 3. Cleanup Commands

#### Safe Cleanup (Recommended)
```bash
# Remove only dangling images
docker image prune -f

# Remove only dangling volumes
docker volume prune -f

# Remove unused networks
docker network prune -f
```

#### Aggressive Cleanup (Use with Caution)
```bash
# Remove ALL unused resources (images, containers, networks, cache)
docker system prune -af

# Remove ALL unused volumes (including named ones not used by containers)
docker volume prune -f
```

#### Build Cache Cleanup
```bash
# Remove build cache
docker builder prune -af

# Remove build cache with size limit
docker builder prune -af --filter "until=24h"
```

### 4. Selective Cleanup

#### Remove Specific Images
```bash
# Remove specific dangling images by ID
docker rmi $(docker images --filter "dangling=true" -q)

# Remove images older than 24 hours
docker image prune -af --filter "until=24h"
```

#### Remove Specific Volumes
```bash
# Remove specific volume by name
docker volume rm volume_name

# Remove multiple volumes
docker volume rm vol1 vol2 vol3
```

### 5. Container Management

#### Stop and Remove Containers
```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all stopped containers
docker container prune -f

# Remove specific container
docker rm container_name_or_id
```

### 6. Complete System Reset (Nuclear Option)
```bash
# WARNING: This removes EVERYTHING
docker system prune -af --volumes
```

## Timeshift Backup Considerations

### Backup Location Structure
```
/run/timeshift/backup/@/var/lib/docker/
├── buildkit/       # Build cache
├── containers/     # Container data
├── image/          # Image metadata
├── overlay2/       # Layer storage (largest)
├── volumes/        # Volume data
└── tmp/           # Temporary files
```

### Safe Backup Cleanup Approach
1. **DO NOT** directly modify timeshift backup Docker directories
2. Clean the live system first, then create new timeshift snapshot
3. If backup cleanup needed, use `docker system prune` BEFORE creating timeshift snapshot

### Checking Backup Sizes
```bash
# Check sizes of Docker directories in timeshift backup
sudo du -sh /run/timeshift/backup/@/var/lib/docker/*

# Check specific directories
sudo du -sh /run/timeshift/backup/@/var/lib/docker/overlay2
sudo du -sh /run/timeshift/backup/@/var/lib/docker/volumes
```

## Monitoring and Maintenance

### Regular Maintenance Schedule
```bash
# Weekly cleanup (add to crontab)
0 2 * * 0 docker system prune -f >/dev/null 2>&1

# Monthly aggressive cleanup
0 3 1 * * docker system prune -af >/dev/null 2>&1
```

### Disk Space Monitoring
```bash
# Check Docker root directory usage
du -sh /var/lib/docker/

# Monitor specific directories
du -sh /var/lib/docker/overlay2/
du -sh /var/lib/docker/volumes/
du -sh /var/lib/docker/containers/
```

## Troubleshooting

### Common Issues

#### "No space left on device"
```bash
# Emergency cleanup
docker system prune -af --volumes
docker builder prune -af
```

#### Large overlay2 directory
```bash
# Check for stopped containers using space
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Size}}"

# Remove stopped containers
docker container prune -f
```

#### Build cache consuming space
```bash
# Check build cache usage
docker system df

# Clear all build cache
docker builder prune -af
```

### Prevention Tips
1. Regularly run `docker system prune -f`
2. Use `.dockerignore` files to reduce build context
3. Use multi-stage builds to reduce final image size
4. Remove development dependencies in production images
5. Use `--rm` flag for temporary containers

## Session Results (July 29, 2025)

### Before Cleanup
- Multiple dangling images (16 total)
- 10 dangling volumes (144.2MB)
- 3.172GB build cache
- System using excessive disk space

### After Cleanup
- Images: 3 active (1.558GB total)
- Volumes: 11 named volumes (5.15GB, but 100% reclaimable)
- Build Cache: 0B
- Containers: 3 active (74B total)

### Commands Used in Session
```bash
docker system df -v
docker images --filter "dangling=true" -q
docker volume ls -f dangling=true
docker system prune -af
docker volume prune -f
docker system df
```

---
*Generated: July 29, 2025*
*Location: /home/user1/shawndev1/helpful_memory_and_test_files/docker_cleanup_guide.md*