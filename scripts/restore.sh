#!/bin/bash

# ================================
# MSA Project - Database Restore Script
# ================================
# Restores MySQL database from backup file
# Usage: ./scripts/restore.sh [backup_file]

set -e

# ================================
# Color Codes
# ================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ================================
# Configuration
# ================================
BACKUP_DIR="./backups"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.dev.yml}"

# Load environment variables
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# ================================
# Functions
# ================================
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_usage() {
    echo "Usage: $0 [backup_file]"
    echo ""
    echo "Arguments:"
    echo "  backup_file    Path to the backup file (.sql or .sql.gz)"
    echo ""
    echo "Examples:"
    echo "  $0 backups/msa_database_20240128_143022.sql"
    echo "  $0 backups/msa_database_20240128_143022.sql.gz"
    echo ""
    echo "If no file is specified, the script will list available backups."
}

list_backups() {
    echo ""
    log_info "Available backup files:"
    echo ""

    if [ -d "$BACKUP_DIR" ]; then
        local count=0
        for file in "$BACKUP_DIR"/*.sql "$BACKUP_DIR"/*.sql.gz 2>/dev/null; do
            if [ -f "$file" ]; then
                local size=$(du -h "$file" | cut -f1)
                local date=$(stat -c %y "$file" 2>/dev/null | cut -d'.' -f1 || stat -f %Sm "$file" 2>/dev/null)
                echo "  $((++count)). $(basename "$file") ($size) - $date"
            fi
        done

        if [ $count -eq 0 ]; then
            log_warning "No backup files found in $BACKUP_DIR"
        fi
    else
        log_error "Backup directory not found: $BACKUP_DIR"
    fi
    echo ""
}

find_mysql_container() {
    local container_id=$(docker ps -qf "name=mysql" | head -n1)

    if [ -z "$container_id" ]; then
        log_error "MySQL container not found. Is it running?"
        log_info "Start the services with: docker-compose -f $COMPOSE_FILE up -d"
        exit 1
    fi

    echo "$container_id"
}

verify_backup_file() {
    local file="$1"

    if [ ! -f "$file" ]; then
        log_error "Backup file not found: $file"
        exit 1
    fi

    # Check file extension
    if [[ ! "$file" =~ \.(sql|sql\.gz)$ ]]; then
        log_error "Invalid file format. Expected .sql or .sql.gz"
        exit 1
    fi

    # Check if file is not empty
    if [ ! -s "$file" ]; then
        log_error "Backup file is empty: $file"
        exit 1
    fi

    log_success "Backup file verified: $file"
}

restore_database() {
    local backup_file="$1"
    local container_id="$2"
    local db_name="${MYSQL_DATABASE:-msa_database}"
    local db_password="${MYSQL_ROOT_PASSWORD:-}"

    if [ -z "$db_password" ]; then
        log_error "MYSQL_ROOT_PASSWORD not set. Please check your .env file."
        exit 1
    fi

    log_info "Starting database restore..."
    log_warning "This will OVERWRITE the current database: $db_name"
    echo ""

    # Confirmation
    read -p "Are you sure you want to continue? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        log_info "Restore cancelled."
        exit 0
    fi

    echo ""
    log_info "Restoring from: $backup_file"

    # Check if compressed
    if [[ "$backup_file" == *.gz ]]; then
        log_info "Decompressing backup file..."
        gunzip -c "$backup_file" | docker exec -i "$container_id" mysql -u root -p"$db_password" "$db_name"
    else
        docker exec -i "$container_id" mysql -u root -p"$db_password" "$db_name" < "$backup_file"
    fi

    if [ $? -eq 0 ]; then
        log_success "Database restored successfully!"
    else
        log_error "Failed to restore database"
        exit 1
    fi
}

restart_services() {
    log_info "Restarting dependent services..."

    docker-compose -f "$COMPOSE_FILE" restart spring-api python-ai 2>/dev/null || true

    log_success "Services restarted"
}

# ================================
# Main
# ================================
main() {
    echo ""
    echo "================================"
    echo "  MSA Database Restore Script"
    echo "================================"
    echo ""

    # Check for help flag
    if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
        show_usage
        exit 0
    fi

    # If no argument, list available backups
    if [ -z "$1" ]; then
        list_backups
        echo "Usage: $0 <backup_file>"
        exit 0
    fi

    local backup_file="$1"

    # Verify backup file
    verify_backup_file "$backup_file"

    # Find MySQL container
    local container_id=$(find_mysql_container)
    log_info "Found MySQL container: $container_id"

    # Restore database
    restore_database "$backup_file" "$container_id"

    # Ask to restart services
    echo ""
    read -p "Restart dependent services (spring-api, python-ai)? (y/N): " restart
    if [[ "$restart" =~ ^[Yy]$ ]]; then
        restart_services
    fi

    echo ""
    log_success "Restore process completed!"
    echo ""
}

# Run main
main "$@"
