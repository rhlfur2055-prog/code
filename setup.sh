#!/bin/bash

# ================================
# MSA Project Setup Script (Bash)
# ================================
# Automated setup for development and production environments
# Supports: Linux, macOS, WSL
# Author: MSA Project Team
# Version: 1.0.0
# ================================

set -e  # Exit on error

# ================================
# Color Codes
# ================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ================================
# Emojis
# ================================
CHECK="✅"
CROSS="❌"
ROCKET="🚀"
GEAR="⚙️"
FOLDER="📂"
DATABASE="🗄️"
LOCK="🔒"
WARNING="⚠️"

# ================================
# Banner
# ================================
print_banner() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║         ${ROCKET}  MSA PROJECT SETUP WIZARD  ${ROCKET}                  ║"
    echo "║                                                            ║"
    echo "║         Automated Deployment & Migration System            ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# ================================
# Logging Functions
# ================================
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}${CHECK} [SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}${WARNING} [WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}${CROSS} [ERROR]${NC} $1"
}

log_step() {
    echo -e "${PURPLE}${GEAR} [STEP]${NC} $1"
}

# ================================
# Progress Bar
# ================================
show_progress() {
    local duration=$1
    local message=$2
    local progress=0
    local total=50
    
    echo -ne "${message} ["
    while [ $progress -le $total ]; do
        echo -ne "="
        progress=$((progress + 1))
        sleep $(echo "scale=2; $duration / $total" | bc)
    done
    echo -e "] ${CHECK}"
}

# ================================
# Prerequisites Check
# ================================
check_prerequisites() {
    log_step "Checking prerequisites..."
    
    local missing_tools=()
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        missing_tools+=("Docker")
    else
        log_success "Docker is installed ($(docker --version))"
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        missing_tools+=("Docker Compose")
    else
        log_success "Docker Compose is installed ($(docker-compose --version))"
    fi
    
    # Check curl
    if ! command -v curl &> /dev/null; then
        missing_tools+=("curl")
    fi
    
    # Check bc (for progress bar)
    if ! command -v bc &> /dev/null; then
        log_warning "bc not found (progress bars will be disabled)"
    fi
    
    # Report missing tools
    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        echo ""
        echo "Please install the missing tools:"
        echo "  - Docker: https://docs.docker.com/get-docker/"
        echo "  - Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    log_success "All prerequisites satisfied!"
    echo ""
}

# ================================
# Environment Selection
# ================================
select_environment() {
    log_step "Select deployment environment"
    echo ""
    echo "Available environments:"
    echo "  ${CYAN}1)${NC} Development (Hot reload, debug ports, verbose logging)"
    echo "  ${CYAN}2)${NC} Production (Optimized, secure, resource-limited)"
    echo ""
    
    while true; do
        read -p "Enter your choice (1 or 2): " env_choice
        case $env_choice in
            1)
                ENVIRONMENT="dev"
                COMPOSE_FILE="docker-compose.dev.yml"
                log_success "Development environment selected"
                break
                ;;
            2)
                ENVIRONMENT="prod"
                COMPOSE_FILE="docker-compose.prod.yml"
                log_success "Production environment selected"
                break
                ;;
            *)
                log_error "Invalid choice. Please enter 1 or 2."
                ;;
        esac
    done
    echo ""
}

# ================================
# Environment File Setup
# ================================
setup_env_file() {
    log_step "Setting up environment variables..."
    
    if [ -f ".env" ]; then
        log_warning ".env file already exists"
        read -p "Do you want to overwrite it? (y/N): " overwrite
        if [[ ! $overwrite =~ ^[Yy]$ ]]; then
            log_info "Using existing .env file"
            return
        fi
    fi
    
    if [ ! -f ".env.example" ]; then
        log_error ".env.example not found!"
        exit 1
    fi
    
    log_info "Copying .env.example to .env..."
    cp .env.example .env
    
    # Interactive configuration
    echo ""
    log_info "Let's configure your environment variables..."
    echo ""
    
    # Database password
    read -sp "Enter MySQL root password: " mysql_password
    echo ""
    if [ -z "$mysql_password" ]; then
        mysql_password="defaultpassword123"
        log_warning "Using default password (CHANGE THIS IN PRODUCTION!)"
    fi
    sed -i.bak "s/your_mysql_password_here/$mysql_password/g" .env
    
    # JWT Secret
    read -p "Enter JWT secret (press Enter for auto-generation): " jwt_secret
    if [ -z "$jwt_secret" ]; then
        jwt_secret=$(openssl rand -base64 32 2>/dev/null || echo "autogenerated_jwt_secret_$(date +%s)")
        log_info "JWT secret auto-generated"
    fi
    sed -i.bak "s/your_jwt_secret_key_change_this_in_production/$jwt_secret/g" .env
    
    # Set environment
    if [ "$ENVIRONMENT" == "prod" ]; then
        sed -i.bak "s/NODE_ENV=development/NODE_ENV=production/g" .env
        sed -i.bak "s/SPRING_PROFILE=dev/SPRING_PROFILE=prod/g" .env
        sed -i.bak "s/FASTAPI_ENV=development/FASTAPI_ENV=production/g" .env
    fi
    
    rm -f .env.bak
    
    log_success "Environment file configured!"
    echo ""
}

# ================================
# Docker Build
# ================================
build_images() {
    log_step "Building Docker images..."
    echo ""
    
    log_info "This may take several minutes on first run..."
    echo ""
    
    if docker-compose -f "$COMPOSE_FILE" build --no-cache; then
        log_success "Docker images built successfully!"
    else
        log_error "Failed to build Docker images"
        exit 1
    fi
    
    echo ""
}

# ================================
# Start Services
# ================================
start_services() {
    log_step "Starting services..."
    echo ""
    
    if docker-compose -f "$COMPOSE_FILE" up -d; then
        log_success "Services started successfully!"
    else
        log_error "Failed to start services"
        exit 1
    fi
    
    echo ""
}

# ================================
# Health Check
# ================================
run_health_check() {
    log_step "Running health checks..."
    echo ""
    
    log_info "Waiting for services to be ready (this may take 1-2 minutes)..."
    sleep 10
    
    # Check each service
    services=(
        "frontend:3000"
        "spring-api:8080/actuator/health"
        "python-ai:8000/health"
    )
    
    for service in "${services[@]}"; do
        IFS=':' read -r name endpoint <<< "$service"
        
        echo -ne "Checking ${CYAN}${name}${NC}... "
        
        max_retries=30
        retry_count=0
        
        while [ $retry_count -lt $max_retries ]; do
            if curl -f -s "http://localhost:${endpoint}" > /dev/null 2>&1; then
                echo -e "${GREEN}${CHECK} Healthy${NC}"
                break
            fi
            
            retry_count=$((retry_count + 1))
            sleep 2
        done
        
        if [ $retry_count -eq $max_retries ]; then
            echo -e "${RED}${CROSS} Unhealthy${NC}"
            log_warning "${name} is not responding. Check logs: docker-compose -f ${COMPOSE_FILE} logs ${name}"
        fi
    done
    
    echo ""
}

# ================================
# Display Summary
# ================================
display_summary() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║                  ${ROCKET} SETUP COMPLETE! ${ROCKET}                       ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    
    log_success "MSA Project is now running!"
    echo ""
    echo "📍 Service URLs:"
    echo "   ${CYAN}Frontend:${NC}     http://localhost:3000"
    echo "   ${CYAN}Spring API:${NC}   http://localhost:8080"
    echo "   ${CYAN}Python AI:${NC}    http://localhost:8000"
    if [ "$ENVIRONMENT" == "dev" ]; then
        echo "   ${CYAN}phpMyAdmin:${NC}   http://localhost:8081"
    fi
    echo ""
    
    echo "📋 Useful commands:"
    echo "   ${YELLOW}View logs:${NC}        docker-compose -f ${COMPOSE_FILE} logs -f"
    echo "   ${YELLOW}Stop services:${NC}    docker-compose -f ${COMPOSE_FILE} down"
    echo "   ${YELLOW}Restart:${NC}          docker-compose -f ${COMPOSE_FILE} restart"
    echo "   ${YELLOW}Health check:${NC}     ./scripts/healthcheck.sh"
    echo "   ${YELLOW}Backup DB:${NC}        ./scripts/backup.sh"
    echo ""
    
    if [ "$ENVIRONMENT" == "prod" ]; then
        echo "${WARNING}  ${YELLOW}PRODUCTION REMINDERS:${NC}"
        echo "   - Ensure firewall is configured"
        echo "   - Set up SSL certificates"
        echo "   - Configure regular backups"
        echo "   - Monitor resource usage"
        echo ""
    fi
}

# ================================
# Cleanup Function
# ================================
cleanup_on_error() {
    log_error "Setup failed. Cleaning up..."
    docker-compose -f "$COMPOSE_FILE" down 2>/dev/null || true
    exit 1
}

# ================================
# Main Execution
# ================================
main() {
    # Set trap for errors
    trap cleanup_on_error ERR
    
    # Clear screen
    clear
    
    # Show banner
    print_banner
    
    # Check prerequisites
    check_prerequisites
    
    # Select environment
    select_environment
    
    # Setup .env file
    setup_env_file
    
    # Build images
    read -p "Do you want to build Docker images? (Y/n): " build_choice
    if [[ ! $build_choice =~ ^[Nn]$ ]]; then
        build_images
    fi
    
    # Start services
    start_services
    
    # Run health checks
    run_health_check
    
    # Display summary
    display_summary
    
    log_success "Setup script completed successfully! ${ROCKET}"
}

# Run main function
main
