# Interactive Install Scripts Guide for LLMs

## Table of Contents
1. [Introduction & Purpose](#introduction--purpose)
2. [Core Components](#core-components)
3. [User Interaction Patterns](#user-interaction-patterns)
4. [Prerequisites & Environment Checks](#prerequisites--environment-checks)
5. [Installation Flow Management](#installation-flow-management)
6. [Data & Configuration Management](#data--configuration-management)
7. [Service Management](#service-management)
8. [User Communication](#user-communication)
9. [Template Examples](#template-examples)
10. [Testing & Debugging](#testing--debugging)

---

## Introduction & Purpose

Interactive install scripts provide guided, user-friendly installation experiences for complex software systems. They bridge the gap between fully automated installations (which may not fit all environments) and manual setup procedures (which are error-prone and time-consuming).

### When to Use Interactive Scripts
- **Complex multi-component systems** with optional features
- **Environment-specific configurations** that require user input
- **Destructive operations** that need explicit confirmation
- **Database migrations or data imports** requiring user choices
- **Development environments** with multiple setup options

### When NOT to Use Interactive Scripts
- Simple single-component installations
- CI/CD automated deployments
- Container image builds
- Systems requiring zero user intervention

---

## Core Components

### Shell Script Foundation
```bash
#!/bin/bash
set -e  # Exit on any error
set -u  # Exit on undefined variables (optional, can break some patterns)
```

### Color Output System
```bash
# ANSI Color Codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Usage examples
echo -e "${GREEN}✅ Success message${NC}"
echo -e "${RED}❌ Error message${NC}"
echo -e "${YELLOW}⚠️  Warning message${NC}"
echo -e "${BLUE}ℹ️  Info message${NC}"
```

### Progress Indicators
```bash
# Spinner function
show_spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Progress dots
show_progress() {
    for i in {1..10}; do
        echo -n "."
        sleep 1
    done
    echo ""
}
```

---

## User Interaction Patterns

### Command Line Arguments
```bash
# Argument parsing with help
while [[ $# -gt 0 ]]; do
    case $1 in
        --clone-production)
            CLONE_PRODUCTION=true
            shift
            ;;
        --skip-backups)
            SKIP_BACKUPS=true
            shift
            ;;
        --config-file)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        --version|-v)
            echo "Version 1.0.0"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --clone-production     Clone production database"
    echo "  --skip-backups         Skip backup creation"
    echo "  --config-file FILE     Use custom config file"
    echo "  --help, -h            Show this help message"
    echo "  --version, -v         Show version information"
    echo ""
    echo "Examples:"
    echo "  $0                     # Interactive installation"
    echo "  $0 --clone-production  # Install with production data"
}
```

### Interactive Prompts with Defaults

#### Yes/No Prompts
```bash
# Yes/No with default to No (safe for destructive actions)
ask_yes_no_default_no() {
    local prompt="$1"
    local response
    
    while true; do
        read -p "${prompt} (y/N): " -r response
        
        # Default to 'n' if user just presses enter
        if [ -z "$response" ]; then
            response="n"
        fi
        
        case $response in
            [Yy]|[Yy][Ee][Ss])
                return 0  # True
                ;;
            [Nn]|[Nn][Oo])
                return 1  # False
                ;;
            *)
                echo "Please answer 'y' for yes or 'n' for no (default: n)"
                ;;
        esac
    done
}

# Yes/No with default to Yes (safe for beneficial actions)
ask_yes_no_default_yes() {
    local prompt="$1"
    local response
    
    while true; do
        read -p "${prompt} (Y/n): " -r response
        
        # Default to 'y' if user just presses enter
        if [ -z "$response" ]; then
            response="y"
        fi
        
        case $response in
            [Yy]|[Yy][Ee][Ss])
                return 0  # True
                ;;
            [Nn]|[Nn][Oo])
                return 1  # False
                ;;
            *)
                echo "Please answer 'y' for yes or 'n' for no (default: y)"
                ;;
        esac
    done
}

# Usage examples
if ask_yes_no_default_no "Delete all existing data?"; then
    echo "User confirmed deletion"
    cleanup_existing_data
else
    echo "Keeping existing data"
fi

if ask_yes_no_default_yes "Install recommended packages?"; then
    install_recommended_packages
fi
```

#### Multiple Choice Prompts
```bash
ask_multiple_choice() {
    local prompt="$1"
    shift
    local options=("$@")
    local choice
    
    echo "$prompt"
    echo ""
    for i in "${!options[@]}"; do
        echo "  $((i+1)). ${options[i]}"
    done
    echo ""
    
    while true; do
        read -p "Enter your choice (1-${#options[@]}): " -r choice
        
        if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#options[@]} ]; then
            return $((choice-1))
        else
            echo "Please enter a number between 1 and ${#options[@]}"
        fi
    done
}

# Usage
database_options=("Fresh installation" "Clone from production" "Restore from backup")
ask_multiple_choice "Choose database setup option:" "${database_options[@]}"
db_choice=$?

case $db_choice in
    0) echo "Fresh installation selected" ;;
    1) echo "Clone from production selected" ;;
    2) echo "Restore from backup selected" ;;
esac
```

#### Input Validation
```bash
ask_input_with_validation() {
    local prompt="$1"
    local validation_pattern="$2"
    local error_msg="$3"
    local default_value="$4"
    local input
    
    while true; do
        if [ -n "$default_value" ]; then
            read -p "${prompt} [${default_value}]: " -r input
            if [ -z "$input" ]; then
                input="$default_value"
            fi
        else
            read -p "${prompt}: " -r input
        fi
        
        if [[ $input =~ $validation_pattern ]]; then
            echo "$input"
            return 0
        else
            echo "$error_msg"
        fi
    done
}

# Usage examples
email=$(ask_input_with_validation "Enter email address" "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$" "Please enter a valid email address")

port=$(ask_input_with_validation "Enter port number" "^[0-9]+$" "Please enter a valid port number" "8080")
```

#### Timeout-Based Prompts (for CI/CD)
```bash
ask_with_timeout() {
    local prompt="$1"
    local timeout="$2"
    local default="$3"
    local response
    
    echo -n "$prompt (default: $default, timeout: ${timeout}s): "
    
    if read -t "$timeout" -r response; then
        if [ -z "$response" ]; then
            response="$default"
        fi
        echo "$response"
    else
        echo ""
        echo "Timeout reached, using default: $default"
        echo "$default"
    fi
}

# Usage
database_name=$(ask_with_timeout "Database name" 30 "myapp")
```

---

## Prerequisites & Environment Checks

### System Requirements Validation
```bash
check_system_requirements() {
    echo -e "${BLUE}📋 Checking system requirements...${NC}"
    
    local failed=false
    
    # Check OS
    if [[ "$OSTYPE" != "linux-gnu"* ]] && [[ "$OSTYPE" != "darwin"* ]]; then
        echo -e "${RED}❌ Unsupported operating system: $OSTYPE${NC}"
        failed=true
    else
        echo -e "${GREEN}✅ Operating system: $OSTYPE${NC}"
    fi
    
    # Check architecture
    arch=$(uname -m)
    if [[ "$arch" != "x86_64" ]] && [[ "$arch" != "arm64" ]]; then
        echo -e "${RED}❌ Unsupported architecture: $arch${NC}"
        failed=true
    else
        echo -e "${GREEN}✅ Architecture: $arch${NC}"
    fi
    
    # Check disk space (example: need 5GB)
    available_space=$(df . | tail -1 | awk '{print $4}')
    required_space=5000000  # 5GB in KB
    if [ "$available_space" -lt "$required_space" ]; then
        echo -e "${RED}❌ Insufficient disk space. Required: 5GB, Available: $((available_space/1000000))GB${NC}"
        failed=true
    else
        echo -e "${GREEN}✅ Disk space: $((available_space/1000000))GB available${NC}"
    fi
    
    if [ "$failed" = true ]; then
        echo -e "${RED}❌ System requirements not met${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ All system requirements satisfied${NC}"
    echo ""
}
```

### Dependency Checks
```bash
check_dependencies() {
    echo -e "${BLUE}🔧 Checking dependencies...${NC}"
    
    local missing_deps=()
    local deps=("docker" "docker compose" "curl" "jq")
    
    for dep in "${deps[@]}"; do
        if ! command -v $dep &> /dev/null; then
            missing_deps+=("$dep")
            echo -e "${RED}❌ Missing: $dep${NC}"
        else
            version=$($dep --version 2>/dev/null | head -1 || echo "version unknown")
            echo -e "${GREEN}✅ Found: $dep ($version)${NC}"
        fi
    done
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo ""
        echo -e "${RED}❌ Missing required dependencies:${NC}"
        for dep in "${missing_deps[@]}"; do
            echo "  • $dep"
        done
        echo ""
        echo "Please install missing dependencies and try again."
        
        # Provide installation hints
        if command -v apt-get &> /dev/null; then
            echo "On Ubuntu/Debian:"
            echo "  sudo apt-get update && sudo apt-get install ${missing_deps[*]}"
        elif command -v yum &> /dev/null; then
            echo "On RHEL/CentOS:"
            echo "  sudo yum install ${missing_deps[*]}"
        elif command -v brew &> /dev/null; then
            echo "On macOS:"
            echo "  brew install ${missing_deps[*]}"
        fi
        
        exit 1
    fi
    
    echo -e "${GREEN}✅ All dependencies satisfied${NC}"
    echo ""
}
```

### Permission Checks
```bash
check_permissions() {
    echo -e "${BLUE}🔐 Checking permissions...${NC}"
    
    # Check if running as root when needed
    if [ "$EUID" -eq 0 ]; then
        echo -e "${YELLOW}⚠️  Running as root${NC}"
        if ask_yes_no_default_no "Continue running as root? (not recommended)"; then
            echo "Proceeding as root..."
        else
            echo "Please run as a regular user with sudo access"
            exit 1
        fi
    fi
    
    # Check sudo access
    if ! sudo -n true 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Some operations require sudo access${NC}"
        sudo -v  # Prompt for password
    fi
    
    # Check write permissions for installation directory
    if [ ! -w "$(pwd)" ]; then
        echo -e "${RED}❌ No write permission in current directory${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Permissions verified${NC}"
    echo ""
}
```

---

## Installation Flow Management

### Modular Function Design
```bash
# Main installation flow
main() {
    # Validate environment
    check_system_requirements
    check_dependencies
    check_permissions
    
    # Handle existing installations
    check_existing_installation
    
    # Get user preferences
    get_installation_preferences
    
    # Backup existing data if needed
    backup_existing_data
    
    # Perform installation
    install_components
    
    # Configure system
    configure_system
    
    # Verify installation
    verify_installation
    
    # Display final information
    show_completion_message
}

# Handle script interruption gracefully
cleanup_on_interrupt() {
    echo ""
    echo -e "${YELLOW}⚠️  Installation interrupted by user${NC}"
    echo "Cleaning up temporary files..."
    
    # Clean up any partial installations
    cleanup_partial_installation
    
    echo -e "${BLUE}ℹ️  Installation cancelled${NC}"
    exit 1
}

trap cleanup_on_interrupt INT TERM
```

### Step Progress Tracking
```bash
# Progress tracking
declare -A INSTALLATION_STEPS=(
    ["check_prereqs"]="Check prerequisites"
    ["backup_data"]="Backup existing data"
    ["install_deps"]="Install dependencies"
    ["configure_system"]="Configure system"
    ["verify_install"]="Verify installation"
)

CURRENT_STEP=1
TOTAL_STEPS=${#INSTALLATION_STEPS[@]}

show_step_progress() {
    local step_key="$1"
    local step_name="${INSTALLATION_STEPS[$step_key]}"
    
    echo -e "${BLUE}📋 Step $CURRENT_STEP/$TOTAL_STEPS: $step_name${NC}"
    echo ""
    
    ((CURRENT_STEP++))
}

# Usage
show_step_progress "check_prereqs"
check_system_requirements
```

### Rollback Capabilities
```bash
# Rollback tracking
ROLLBACK_ACTIONS=()

add_rollback_action() {
    local action="$1"
    ROLLBACK_ACTIONS+=("$action")
}

execute_rollback() {
    echo -e "${YELLOW}🔄 Rolling back changes...${NC}"
    
    # Execute rollback actions in reverse order
    for ((i=${#ROLLBACK_ACTIONS[@]}-1; i>=0; i--)); do
        echo "  • ${ROLLBACK_ACTIONS[i]}"
        eval "${ROLLBACK_ACTIONS[i]}"
    done
    
    echo -e "${GREEN}✅ Rollback completed${NC}"
}

# Usage
create_backup() {
    cp important_file important_file.backup
    add_rollback_action "rm -f important_file.backup"
}
```

---

## Data & Configuration Management

### Backup Strategies
```bash
create_backup() {
    local source="$1"
    local backup_dir="./backups/$(date +%Y%m%d_%H%M%S)"
    
    echo -e "${BLUE}💾 Creating backup...${NC}"
    
    mkdir -p "$backup_dir"
    
    if [ -f "$source" ]; then
        cp "$source" "$backup_dir/"
        echo "  • File backup: $source -> $backup_dir/"
    elif [ -d "$source" ]; then
        cp -r "$source" "$backup_dir/"
        echo "  • Directory backup: $source -> $backup_dir/"
    fi
    
    # Store backup location for rollback
    add_rollback_action "restore_backup '$backup_dir' '$source'"
    
    echo -e "${GREEN}✅ Backup created: $backup_dir${NC}"
}

restore_backup() {
    local backup_dir="$1"
    local target="$2"
    
    echo -e "${YELLOW}📂 Restoring from backup...${NC}"
    
    if [ -d "$backup_dir" ]; then
        rm -rf "$target"
        cp -r "$backup_dir/"* "$(dirname "$target")/"
        echo -e "${GREEN}✅ Backup restored${NC}"
    else
        echo -e "${RED}❌ Backup not found: $backup_dir${NC}"
    fi
}
```

### Configuration Updates
```bash
update_config_file() {
    local config_file="$1"
    local key="$2"
    local value="$3"
    local backup_created=false
    
    # Create backup if not already done
    if [ ! -f "${config_file}.backup" ]; then
        cp "$config_file" "${config_file}.backup"
        add_rollback_action "mv '${config_file}.backup' '$config_file'"
        backup_created=true
    fi
    
    # Update configuration
    if grep -q "^${key}=" "$config_file"; then
        # Key exists, replace it
        sed -i "s/^${key}=.*/${key}=${value}/" "$config_file"
        echo "  • Updated: $key=$value"
    else
        # Key doesn't exist, add it
        echo "${key}=${value}" >> "$config_file"
        echo "  • Added: $key=$value"
    fi
    
    if [ "$backup_created" = true ]; then
        echo "  • Backup created: ${config_file}.backup"
    fi
}

# Database-specific configuration
update_database_credentials() {
    local env_file=".env"
    local db_password="$1"
    local db_name="$2"
    
    echo -e "${BLUE}🔧 Updating database configuration...${NC}"
    
    update_config_file "$env_file" "POSTGRES_PASSWORD" "$db_password"
    update_config_file "$env_file" "POSTGRES_DB" "$db_name"
    update_config_file "$env_file" "DATABASE_URL" "postgres://user:${db_password}@localhost:5432/${db_name}"
    
    echo -e "${GREEN}✅ Database configuration updated${NC}"
}
```

---

## Service Management

### Service Health Checks
```bash
wait_for_service() {
    local service_name="$1"
    local health_check_command="$2"
    local timeout="${3:-60}"
    local interval="${4:-2}"
    
    echo -e "${BLUE}⏳ Waiting for $service_name to be ready...${NC}"
    
    local elapsed=0
    local max_dots=20
    local dot_interval=$((timeout / max_dots))
    local dots_shown=0
    
    while [ $elapsed -lt $timeout ]; do
        if eval "$health_check_command" >/dev/null 2>&1; then
            echo ""
            echo -e "${GREEN}✅ $service_name is ready${NC}"
            return 0
        fi
        
        # Show progress dots
        if [ $((elapsed % dot_interval)) -eq 0 ] && [ $dots_shown -lt $max_dots ]; then
            echo -n "."
            ((dots_shown++))
        fi
        
        sleep $interval
        elapsed=$((elapsed + interval))
    done
    
    echo ""
    echo -e "${RED}❌ $service_name failed to become ready within $timeout seconds${NC}"
    return 1
}

# Usage examples
wait_for_service "PostgreSQL" "docker exec myapp-postgres pg_isready -U postgres"
wait_for_service "Web Server" "curl -s http://localhost:8080/health"
wait_for_service "API" "curl -s http://localhost:3000/api/ping | grep -q 'pong'"
```

### Service Management Functions
```bash
start_services() {
    echo -e "${BLUE}🚀 Starting services...${NC}"
    
    # Start in dependency order
    services=("database" "cache" "api" "web")
    
    for service in "${services[@]}"; do
        echo "  • Starting $service..."
        docker compose up -d "$service"
        
        # Service-specific health checks
        case $service in
            "database")
                wait_for_service "Database" "docker exec myapp-db pg_isready -U postgres"
                ;;
            "cache")
                wait_for_service "Cache" "docker exec myapp-redis redis-cli ping | grep -q PONG"
                ;;
            "api")
                wait_for_service "API" "curl -s http://localhost:3000/health"
                ;;
            "web")
                wait_for_service "Web" "curl -s http://localhost:8080"
                ;;
        esac
    done
    
    echo -e "${GREEN}✅ All services started successfully${NC}"
}

stop_services() {
    echo -e "${YELLOW}🛑 Stopping services...${NC}"
    docker compose down
    echo -e "${GREEN}✅ Services stopped${NC}"
}
```

---

## User Communication

### Clear Status Messages
```bash
# Status message templates
show_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

show_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

show_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

show_error() {
    echo -e "${RED}❌ $1${NC}"
}

show_step() {
    echo -e "${PURPLE}👉 $1${NC}"
}

# Section headers
show_section() {
    local title="$1"
    local width=50
    local padding=$((($width - ${#title}) / 2))
    
    echo ""
    echo -e "${BLUE}$(printf '=%.0s' $(seq 1 $width))${NC}"
    echo -e "${BLUE}$(printf '%*s' $padding)$title${NC}"
    echo -e "${BLUE}$(printf '=%.0s' $(seq 1 $width))${NC}"
    echo ""
}
```

### Help Documentation
```bash
show_detailed_help() {
    cat << EOF
INSTALLATION SCRIPT HELP
========================

OVERVIEW:
This script installs and configures MyApp with all necessary components.

USAGE:
  $0 [OPTIONS]

OPTIONS:
  --clone-production     Clone production database to development
  --skip-backups        Skip backup creation (not recommended)
  --config-file FILE    Use custom configuration file
  --port PORT           Set custom port (default: 8080)
  --help, -h           Show this help message
  --version, -v        Show version information

EXAMPLES:
  # Interactive installation with all prompts
  $0

  # Silent installation with production data
  $0 --clone-production --skip-backups

  # Installation with custom configuration
  $0 --config-file ./my-config.env --port 3000

ENVIRONMENT VARIABLES:
  DB_PASSWORD          Database password (if not set, will prompt)
  ADMIN_EMAIL          Administrator email (if not set, will prompt)
  SKIP_CONFIRMATION   Skip confirmation prompts (yes/no)

FILES CREATED:
  .env                 Environment configuration
  ./backups/           Backup directory (if backups enabled)
  ./logs/              Application logs

NETWORK PORTS:
  8080                 Web interface (customizable with --port)
  5432                 Database (internal)
  6379                 Cache (internal)

TROUBLESHOOTING:
  • Check system requirements with: docker --version
  • View logs with: docker compose logs
  • Reset installation: docker compose down -v

SUPPORT:
  Documentation: https://example.com/docs
  Issues: https://github.com/example/myapp/issues

EOF
}
```

### Error Messages with Solutions
```bash
handle_error() {
    local error_code="$1"
    local error_message="$2"
    
    show_error "$error_message"
    echo ""
    
    case $error_code in
        "DOCKER_NOT_FOUND")
            echo -e "${BLUE}💡 Solution:${NC}"
            echo "  Install Docker by following the official guide:"
            echo "  https://docs.docker.com/get-docker/"
            ;;
        "INSUFFICIENT_SPACE")
            echo -e "${BLUE}💡 Solutions:${NC}"
            echo "  • Free up disk space by removing unused files"
            echo "  • Use 'docker system prune' to clean up Docker resources"
            echo "  • Choose a different installation directory with more space"
            ;;
        "PERMISSION_DENIED")
            echo -e "${BLUE}💡 Solutions:${NC}"
            echo "  • Run: sudo chmod +x $0"
            echo "  • Ensure you have write access to the current directory"
            echo "  • Add your user to the docker group: sudo usermod -aG docker $USER"
            ;;
        "SERVICE_FAILED")
            echo -e "${BLUE}💡 Troubleshooting:${NC}"
            echo "  • Check logs: docker compose logs"
            echo "  • Verify port availability: netstat -tlnp | grep :8080"
            echo "  • Restart services: docker compose restart"
            ;;
        *)
            echo -e "${BLUE}💡 General troubleshooting:${NC}"
            echo "  • Check the logs in ./logs/ directory"
            echo "  • Run with --help for more options"
            echo "  • Contact support with error details"
            ;;
    esac
    echo ""
}
```

### Final Success Summary
```bash
show_completion_message() {
    show_section "INSTALLATION COMPLETE"
    
    echo -e "${GREEN}🎉 MyApp has been successfully installed!${NC}"
    echo ""
    
    echo -e "${BLUE}📍 Service URLs:${NC}"
    echo "  🌐 Web Interface:     http://localhost:${PORT}"
    echo "  📊 Admin Dashboard:   http://localhost:${PORT}/admin"
    echo "  📚 API Documentation: http://localhost:${PORT}/docs"
    echo ""
    
    if [ "$DATABASE_CLONED" = true ]; then
        echo -e "${BLUE}👤 Access Information (Production Data Cloned):${NC}"
        echo "  • Use existing production credentials"
        echo "  • All production data is available"
    else
        echo -e "${BLUE}👤 Administrator Credentials:${NC}"
        echo "  Username: admin"
        echo "  Password: ${ADMIN_PASSWORD}"
        echo "  Email: ${ADMIN_EMAIL}"
    fi
    echo ""
    
    echo -e "${BLUE}🔧 Management Commands:${NC}"
    echo "  docker compose logs -f        View logs"
    echo "  docker compose down           Stop services"
    echo "  docker compose up -d          Start services"
    echo "  docker compose restart        Restart services"
    echo ""
    
    echo -e "${BLUE}📁 Important Files:${NC}"
    echo "  .env                          Environment configuration"
    echo "  docker-compose.yml            Service definitions"
    echo "  ./backups/                    Data backups"
    echo "  ./logs/                       Application logs"
    echo ""
    
    echo -e "${BLUE}🔍 Next Steps:${NC}"
    echo "  1. Open http://localhost:${PORT} in your browser"
    echo "  2. Log in with the credentials above"
    echo "  3. Complete the initial setup wizard"
    echo "  4. Configure your first project"
    echo ""
    
    echo -e "${YELLOW}⚠️  Important Notes:${NC}"
    echo "  • Change default passwords before production use"
    echo "  • Configure regular backups for important data"
    echo "  • Monitor logs for any errors: docker compose logs"
    echo ""
    
    echo -e "${GREEN}🎯 Installation Summary:${NC}"
    echo "  • Total installation time: $((SECONDS / 60)) minutes"
    echo "  • Components installed: Database, Cache, API, Web UI"
    echo "  • Database: $([ "$DATABASE_CLONED" = true ] && echo "Cloned from production" || echo "Fresh installation")"
    echo "  • Backups: $([ "$SKIP_BACKUPS" = true ] && echo "Disabled" || echo "Created")"
    echo ""
    
    echo -e "${BLUE}📞 Support:${NC}"
    echo "  Documentation: https://docs.example.com"
    echo "  Community: https://community.example.com"  
    echo "  Issues: https://github.com/example/myapp/issues"
    echo ""
    
    echo -e "${GREEN}Happy coding! 🚀${NC}"
}
```

---

## Template Examples

### Basic Interactive Installer
```bash
#!/bin/bash
set -e

# Basic installer template
PROJECT_NAME="myapp"
DEFAULT_PORT=8080
INSTALL_DIR="$(pwd)"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

main() {
    echo -e "${BLUE}🚀 $PROJECT_NAME Installer${NC}"
    echo "================================"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Get user preferences
    get_preferences
    
    # Install
    perform_installation
    
    # Show completion
    show_completion
}

check_prerequisites() {
    echo -e "${BLUE}📋 Checking prerequisites...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is required but not installed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Prerequisites satisfied${NC}"
    echo ""
}

get_preferences() {
    echo -e "${BLUE}⚙️  Configuration${NC}"
    echo ""
    
    # Get port
    read -p "Port number [$DEFAULT_PORT]: " PORT
    PORT=${PORT:-$DEFAULT_PORT}
    
    # Get admin email
    while true; do
        read -p "Administrator email: " ADMIN_EMAIL
        if [[ $ADMIN_EMAIL =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
            break
        else
            echo "Please enter a valid email address"
        fi
    done
    
    echo ""
}

perform_installation() {
    echo -e "${BLUE}📦 Installing $PROJECT_NAME...${NC}"
    
    # Create configuration
    cat > .env << EOF
PORT=$PORT
ADMIN_EMAIL=$ADMIN_EMAIL
POSTGRES_PASSWORD=$(openssl rand -base64 32)
EOF
    
    # Start services
    docker compose up -d
    
    echo -e "${GREEN}✅ Installation completed${NC}"
    echo ""
}

show_completion() {
    echo -e "${GREEN}🎉 $PROJECT_NAME is ready!${NC}"
    echo ""
    echo "Access your application at: http://localhost:$PORT"
    echo "Administrator email: $ADMIN_EMAIL"
    echo ""
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

### Docker-Based Service Installer
```bash
#!/bin/bash
set -e

# Docker service installer template
SERVICE_NAME="myservice"
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"

# State tracking
SERVICES_STARTED=false
CLEANUP_REGISTERED=false

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

cleanup_on_exit() {
    if [ "$SERVICES_STARTED" = true ]; then
        echo -e "\n${YELLOW}🧹 Cleaning up...${NC}"
        docker compose down -v
    fi
}

register_cleanup() {
    if [ "$CLEANUP_REGISTERED" = false ]; then
        trap cleanup_on_exit EXIT INT TERM
        CLEANUP_REGISTERED=true
    fi
}

main() {
    echo -e "${BLUE}🚀 $SERVICE_NAME Docker Installer${NC}"
    echo "===================================="
    echo ""
    
    register_cleanup
    
    # Validate environment
    validate_environment
    
    # Handle existing installation
    handle_existing_installation
    
    # Get configuration
    configure_services
    
    # Install and start
    install_services
    
    # Verify installation
    verify_installation
    
    # Success
    show_completion
}

validate_environment() {
    echo -e "${BLUE}🔍 Validating environment...${NC}"
    
    # Check Docker and Docker Compose
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker not found${NC}"
        exit 1
    fi
    
    if ! docker compose version &> /dev/null; then
        echo -e "${RED}❌ Docker Compose not found${NC}"
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker daemon not running${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Environment validated${NC}"
    echo ""
}

handle_existing_installation() {
    # Check for existing containers
    existing=$(docker ps -a --filter "name=${SERVICE_NAME}-" --format "{{.Names}}" 2>/dev/null || true)
    
    if [ -n "$existing" ]; then
        echo -e "${YELLOW}⚠️  Found existing $SERVICE_NAME containers:${NC}"
        echo "$existing" | sed 's/^/  • /'
        echo ""
        
        if ask_yes_no_default_no "Remove existing installation and start fresh?"; then
            echo -e "${YELLOW}🗑️  Removing existing containers...${NC}"
            docker compose down -v 2>/dev/null || true
            echo -e "${GREEN}✅ Cleanup completed${NC}"
        else
            echo -e "${BLUE}ℹ️  Continuing with existing installation${NC}"
        fi
        echo ""
    fi
}

configure_services() {
    echo -e "${BLUE}⚙️  Service Configuration${NC}"
    echo ""
    
    # Database configuration
    DB_NAME=$(ask_input_with_default "Database name" "$SERVICE_NAME")
    DB_USER=$(ask_input_with_default "Database user" "$SERVICE_NAME")
    DB_PASSWORD=$(ask_input_with_default "Database password" "$(openssl rand -base64 16)")
    
    # Application configuration
    APP_PORT=$(ask_input_with_default "Application port" "8080")
    APP_ENV=$(ask_choice "Environment" "development" "production")
    
    # Create .env file
    cat > "$ENV_FILE" << EOF
# Database Configuration
POSTGRES_DB=$DB_NAME
POSTGRES_USER=$DB_USER
POSTGRES_PASSWORD=$DB_PASSWORD

# Application Configuration
APP_PORT=$APP_PORT
APP_ENV=$APP_ENV
NODE_ENV=$APP_ENV

# Generated
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@postgres:5432/$DB_NAME
EOF
    
    echo -e "${GREEN}✅ Configuration saved to $ENV_FILE${NC}"
    echo ""
}

install_services() {
    echo -e "${BLUE}📦 Installing services...${NC}"
    
    # Pull images first
    echo "  • Pulling Docker images..."
    docker compose pull
    
    # Build custom images if needed
    echo "  • Building custom images..."
    docker compose build
    
    # Start services
    echo "  • Starting services..."
    docker compose up -d
    SERVICES_STARTED=true
    
    echo -e "${GREEN}✅ Services started${NC}"
    echo ""
}

verify_installation() {
    echo -e "${BLUE}🔍 Verifying installation...${NC}"
    
    # Wait for database
    wait_for_service "Database" "docker compose exec -T postgres pg_isready -U $DB_USER" 60
    
    # Wait for application
    wait_for_service "Application" "curl -f http://localhost:$APP_PORT/health" 90
    
    echo -e "${GREEN}✅ All services verified${NC}"
    echo ""
}

show_completion() {
    echo -e "${GREEN}🎉 $SERVICE_NAME installation completed!${NC}"
    echo ""
    echo -e "${BLUE}📍 Services:${NC}"
    echo "  🌐 Application: http://localhost:$APP_PORT"
    echo "  🗃️  Database:   localhost:5432"
    echo ""
    echo -e "${BLUE}📁 Configuration:${NC}"
    echo "  Environment: $ENV_FILE"
    echo "  Services:    $COMPOSE_FILE"
    echo ""
    echo -e "${BLUE}🔧 Management:${NC}"
    echo "  View logs:    docker compose logs -f"
    echo "  Stop services: docker compose down"
    echo "  Restart:      docker compose restart"
    echo ""
}

# Utility functions (include ask_yes_no_default_no, ask_input_with_default, etc.)
# ... (previous utility functions here)

# Run main function
main "$@"
```

### Database Migration Script
```bash
#!/bin/bash
set -e

# Database migration installer template
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
MIGRATION_DIR="./migrations"
BACKUP_DIR="./backups"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

main() {
    echo -e "${BLUE}🗃️  Database Migration Installer${NC}"
    echo "=================================="
    echo ""
    
    # Get database connection info
    get_database_config
    
    # Test connection
    test_database_connection
    
    # Check migration status
    check_migration_status
    
    # Create backup
    create_backup
    
    # Run migrations
    run_migrations
    
    # Verify migrations
    verify_migrations
    
    # Show completion
    show_completion
}

get_database_config() {
    echo -e "${BLUE}🔧 Database Configuration${NC}"
    echo ""
    
    DB_HOST=$(ask_input_with_default "Database host" "$DB_HOST")
    DB_PORT=$(ask_input_with_default "Database port" "$DB_PORT")
    DB_NAME=$(ask_input_required "Database name")
    DB_USER=$(ask_input_required "Database user")
    
    # Get password securely
    echo -n "Database password: "
    read -s DB_PASSWORD
    echo ""
    echo ""
}

test_database_connection() {
    echo -e "${BLUE}🔌 Testing database connection...${NC}"
    
    # Test connection using psql
    export PGPASSWORD="$DB_PASSWORD"
    
    if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" &> /dev/null; then
        echo -e "${GREEN}✅ Database connection successful${NC}"
    else
        echo -e "${RED}❌ Database connection failed${NC}"
        echo "Please check your connection parameters and try again."
        exit 1
    fi
    echo ""
}

check_migration_status() {
    echo -e "${BLUE}📊 Checking migration status...${NC}"
    
    # Create migration tracking table if it doesn't exist
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version VARCHAR(255) PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    " &> /dev/null
    
    # Get applied migrations
    applied_migrations=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT version FROM schema_migrations ORDER BY version;" 2>/dev/null | tr -d ' ')
    
    # Get available migrations
    available_migrations=()
    if [ -d "$MIGRATION_DIR" ]; then
        while IFS= read -r -d '' file; do
            basename=$(basename "$file" .sql)
            available_migrations+=("$basename")
        done < <(find "$MIGRATION_DIR" -name "*.sql" -print0 | sort -z)
    fi
    
    # Find pending migrations
    pending_migrations=()
    for migration in "${available_migrations[@]}"; do
        if ! echo "$applied_migrations" | grep -q "^$migration$"; then
            pending_migrations+=("$migration")
        fi
    done
    
    echo "  • Applied migrations: ${#applied_migrations[@]}"
    echo "  • Available migrations: ${#available_migrations[@]}"
    echo "  • Pending migrations: ${#pending_migrations[@]}"
    
    if [ ${#pending_migrations[@]} -eq 0 ]; then
        echo -e "${GREEN}✅ Database is up to date${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  Found ${#pending_migrations[@]} pending migrations${NC}"
        for migration in "${pending_migrations[@]}"; do
            echo "    • $migration"
        done
    fi
    echo ""
}

create_backup() {
    if ask_yes_no_default_yes "Create database backup before migration?"; then
        echo -e "${BLUE}💾 Creating database backup...${NC}"
        
        mkdir -p "$BACKUP_DIR"
        backup_file="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
        
        pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" > "$backup_file"
        
        echo -e "${GREEN}✅ Backup created: $backup_file${NC}"
        echo ""
    fi
}

run_migrations() {
    echo -e "${BLUE}🚀 Running migrations...${NC}"
    
    local failed_migrations=()
    
    for migration in "${pending_migrations[@]}"; do
        echo "  • Applying: $migration"
        
        migration_file="$MIGRATION_DIR/$migration.sql"
        
        if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$migration_file" &> /dev/null; then
            # Mark as applied
            psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "INSERT INTO schema_migrations (version) VALUES ('$migration');" &> /dev/null
            echo -e "    ${GREEN}✅ Success${NC}"
        else
            echo -e "    ${RED}❌ Failed${NC}"
            failed_migrations+=("$migration")
        fi
    done
    
    if [ ${#failed_migrations[@]} -gt 0 ]; then
        echo ""
        echo -e "${RED}❌ Migration failures:${NC}"
        for migration in "${failed_migrations[@]}"; do
            echo "  • $migration"
        done
        
        if ask_yes_no_default_no "Continue despite failures?"; then
            echo "Continuing with partial migration..."
        else
            echo "Migration stopped due to failures."
            exit 1
        fi
    fi
    
    echo ""
}

verify_migrations() {
    echo -e "${BLUE}🔍 Verifying migrations...${NC}"
    
    # Re-check migration status
    applied_count=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM schema_migrations;" | tr -d ' ')
    
    echo "  • Total applied migrations: $applied_count"
    
    # Run any verification queries if they exist
    if [ -f "$MIGRATION_DIR/verify.sql" ]; then
        echo "  • Running verification queries..."
        if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$MIGRATION_DIR/verify.sql" &> /dev/null; then
            echo -e "${GREEN}    ✅ Verification passed${NC}"
        else
            echo -e "${YELLOW}    ⚠️  Verification queries failed${NC}"
        fi
    fi
    
    echo -e "${GREEN}✅ Migration verification completed${NC}"
    echo ""
}

show_completion() {
    echo -e "${GREEN}🎉 Database migration completed!${NC}"
    echo ""
    echo -e "${BLUE}📊 Summary:${NC}"
    echo "  • Database: $DB_NAME"
    echo "  • Host: $DB_HOST:$DB_PORT"
    echo "  • Migrations applied: ${#pending_migrations[@]}"
    
    if [ -n "$backup_file" ]; then
        echo "  • Backup: $backup_file"
    fi
    
    echo ""
    echo -e "${BLUE}💡 Next steps:${NC}"
    echo "  • Test your application with the updated database"
    echo "  • Monitor for any issues in production"
    echo "  • Keep the backup file until you're confident the migration succeeded"
    echo ""
}

# Include utility functions here...

# Run main function
main "$@"
```

---

## Testing & Debugging

### Dry-Run Mode
```bash
# Dry-run functionality
DRY_RUN=false

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                echo -e "${YELLOW}🧪 DRY RUN MODE - No changes will be made${NC}"
                shift
                ;;
            # ... other arguments
        esac
    done
}

execute_command() {
    local command="$1"
    local description="$2"
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[DRY RUN] Would execute: $command${NC}"
        if [ -n "$description" ]; then
            echo -e "${YELLOW}[DRY RUN] Purpose: $description${NC}"
        fi
        return 0
    else
        echo "Executing: $description"
        eval "$command"
    fi
}

# Usage
execute_command "docker compose up -d" "Start all services"
execute_command "psql -c 'CREATE DATABASE myapp'" "Create application database"
```

### Debug Output Options
```bash
# Debug mode
DEBUG=false
VERBOSE=false

# Enable based on arguments or environment
if [[ "$*" == *"--debug"* ]] || [[ "$DEBUG_INSTALL" == "true" ]]; then
    DEBUG=true
fi

if [[ "$*" == *"--verbose"* ]] || [[ "$VERBOSE_INSTALL" == "true" ]]; then
    VERBOSE=true
fi

debug() {
    if [ "$DEBUG" = true ]; then
        echo -e "${PURPLE}[DEBUG] $1${NC}" >&2
    fi
}

verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${CYAN}[VERBOSE] $1${NC}"
    fi
}

# Enhanced command execution with debug info
execute_with_debug() {
    local command="$1"
    local description="$2"
    
    verbose "Starting: $description"
    debug "Command: $command"
    debug "Working directory: $(pwd)"
    debug "Environment: $(printenv | grep -E '^(PATH|HOME|USER)=' | tr '\n' ' ')"
    
    local start_time=$(date +%s)
    
    if eval "$command"; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        debug "Command completed in ${duration}s"
        verbose "Completed: $description"
        return 0
    else
        local exit_code=$?
        debug "Command failed with exit code $exit_code"
        echo -e "${RED}❌ Failed: $description${NC}"
        return $exit_code
    fi
}
```

### Idempotency Considerations
```bash
# Idempotent operations - safe to run multiple times

create_directory_if_missing() {
    local dir="$1"
    local permissions="$2"
    
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        if [ -n "$permissions" ]; then
            chmod "$permissions" "$dir"
        fi
        echo "Created directory: $dir"
    else
        debug "Directory already exists: $dir"
    fi
}

install_package_if_missing() {
    local package="$1"
    
    if ! command -v "$package" &> /dev/null; then
        echo "Installing $package..."
        if command -v apt-get &> /dev/null; then
            apt-get update && apt-get install -y "$package"
        elif command -v yum &> /dev/null; then
            yum install -y "$package"
        else
            echo "Cannot install $package - no package manager found"
            return 1
        fi
    else
        debug "Package already installed: $package"
    fi
}

configure_if_needed() {
    local config_file="$1"
    local config_key="$2"
    local config_value="$3"
    
    if [ ! -f "$config_file" ] || ! grep -q "^${config_key}=" "$config_file" 2>/dev/null; then
        echo "Configuring $config_key in $config_file"
        echo "${config_key}=${config_value}" >> "$config_file"
    else
        # Check if value needs updating
        current_value=$(grep "^${config_key}=" "$config_file" | cut -d'=' -f2-)
        if [ "$current_value" != "$config_value" ]; then
            echo "Updating $config_key in $config_file"
            sed -i "s/^${config_key}=.*/${config_key}=${config_value}/" "$config_file"
        else
            debug "Configuration already correct: $config_key=$config_value"
        fi
    fi
}

# Idempotent service management
ensure_service_running() {
    local service="$1"
    
    if docker compose ps "$service" | grep -q "Up"; then
        debug "Service already running: $service"
        return 0
    else
        echo "Starting service: $service"
        docker compose up -d "$service"
        wait_for_service "$service" "docker compose exec $service echo 'ready'"
    fi
}
```

### Error Recovery and Logging
```bash
# Comprehensive error handling and logging
LOG_FILE="./install.log"
ERROR_LOG="./install_errors.log"

# Initialize logging
exec 1> >(tee -a "$LOG_FILE")
exec 2> >(tee -a "$ERROR_LOG")

log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

log_error() {
    log "ERROR" "$*"
    echo -e "${RED}❌ Error: $*${NC}"
}

log_warning() {
    log "WARN" "$*"
    echo -e "${YELLOW}⚠️  Warning: $*${NC}"
}

log_info() {
    log "INFO" "$*"
    echo -e "${BLUE}ℹ️  $*${NC}"
}

# Error recovery strategies
retry_command() {
    local max_attempts="$1"
    local delay="$2"
    shift 2
    local command="$*"
    
    local attempt=1
    while [ $attempt -le $max_attempts ]; do
        log_info "Attempt $attempt/$max_attempts: $command"
        
        if eval "$command"; then
            log_info "Command succeeded on attempt $attempt"
            return 0
        else
            local exit_code=$?
            log_warning "Attempt $attempt failed with exit code $exit_code"
            
            if [ $attempt -lt $max_attempts ]; then
                log_info "Waiting ${delay}s before retry..."
                sleep "$delay"
            fi
            
            ((attempt++))
        fi
    done
    
    log_error "Command failed after $max_attempts attempts: $command"
    return 1
}

# Usage examples
retry_command 3 5 "curl -f http://localhost:8080/health"
retry_command 5 2 "docker compose up -d database"
```

---

## Best Practices Summary

### 1. **Always Provide Defaults**
- Use safe defaults for destructive actions (default to "No")
- Use convenient defaults for beneficial actions (default to "Yes")
- Clearly indicate defaults in prompts: `(Y/n)` or `(y/N)`

### 2. **Validate User Input**
- Check email formats, port ranges, file paths
- Provide clear error messages for invalid input
- Allow users to retry input rather than exiting

### 3. **Handle Interruptions Gracefully**
- Register cleanup functions with `trap`
- Provide rollback capabilities for partial installations
- Clean up temporary files and containers

### 4. **Provide Clear Feedback**
- Use colors and icons for better visual feedback
- Show progress for long-running operations
- Explain what each step accomplishes

### 5. **Make Scripts Idempotent**
- Safe to run multiple times
- Check existing state before making changes
- Update rather than duplicate configurations

### 6. **Include Comprehensive Help**
- Provide `--help` and `--version` options
- Include usage examples in help text
- Document environment variables and files created

### 7. **Plan for Debugging**
- Include `--dry-run` and `--debug` modes
- Log important operations to files
- Provide troubleshooting information in error messages

### 8. **Consider Different User Types**
- Support both interactive and non-interactive usage
- Provide command-line options for automation
- Include environment variable overrides

This guide provides a comprehensive foundation for creating professional, user-friendly interactive installation scripts that can handle complex deployment scenarios while maintaining excellent user experience.