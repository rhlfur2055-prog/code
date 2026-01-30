#!/bin/bash

# ================================
# MSA Project - Enhanced Database Backup Script
# ================================
# Features:
# - Timestamped backups
# - Optional compression (gzip)
# - Automatic cleanup of old backups
# - Integrity verification
# - Configurable retention period

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
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="${MYSQL_DATABASE:-msa_database}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"
COMPRESS="${COMPRESS_BACKUP:-true}"

# Load environment variables
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Filename
if [ "$COMPRESS" = "true" ]; then
    FILENAME="${DB_NAME}_${TIMESTAMP}.sql.gz"
else
    FILENAME="${DB_NAME}_${TIMESTAMP}.sql"
fi

BACKUP_PATH="${BACKUP_DIR}/${FILENAME}"

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

# Ensure backup directory exists
ensure_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        log_info "Creating backup directory: $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR"
    fi
}

# Find MySQL container
find_mysql_container() {
    local container_id=$(docker ps -qf "name=mysql" | head -n1)

    if [ -z "$container_id" ]; then
        log_error "MySQL container not found. Is it running?"
        log_info "Start the services first: docker-compose up -d"
        exit 1
    fi

    echo "$container_id"
}

# Create backup
create_backup() {
    local container_id="$1"
    local db_password="${MYSQL_ROOT_PASSWORD:-}"

    if [ -z "$db_password" ]; then
        log_error "MYSQL_ROOT_PASSWORD not set. Please check your .env file."
        exit 1
    fi

    log_info "Creating backup of database: $DB_NAME"
    log_info "Backup file: $BACKUP_PATH"

    if [ "$COMPRESS" = "true" ]; then
        log_info "Compression enabled (gzip)"
        docker exec "$container_id" /usr/bin/mysqldump \
            -u root \
            --password="$db_password" \
            --single-transaction \
            --routines \
            --triggers \
            --databases "$DB_NAME" | gzip > "$BACKUP_PATH"
    else
        docker exec "$container_id" /usr/bin/mysqldump \
            -u root \
            --password="$db_password" \
            --single-transaction \
            --routines \
            --triggers \
            --databases "$DB_NAME" > "$BACKUP_PATH"
    fi

    if [ $? -eq 0 ]; then
        local size=$(du -h "$BACKUP_PATH" | cut -f1)
        log_success "Backup created successfully: $BACKUP_PATH ($size)"
    else
        log_error "Backup failed!"
        rm -f "$BACKUP_PATH"
        exit 1
    fi
}

# Verify backup integrity
verify_backup() {
    log_info "Verifying backup integrity..."

    if [ ! -f "$BACKUP_PATH" ]; then
        log_error "Backup file not found!"
        exit 1
    fi

    local size=$(stat -f%z "$BACKUP_PATH" 2>/dev/null || stat -c%s "$BACKUP_PATH" 2>/dev/null)

    if [ "$size" -lt 100 ]; then
        log_error "Backup file is too small (possibly corrupted)"
        exit 1
    fi

    # Check if file can be read
    if [ "$COMPRESS" = "true" ]; then
        if gunzip -t "$BACKUP_PATH" 2>/dev/null; then
            log_success "Backup integrity verified (gzip OK)"
        else
            log_error "Backup file is corrupted (gzip test failed)"
            exit 1
        fi
    else
        if head -n1 "$BACKUP_PATH" | grep -q "MySQL\|mysqldump\|--"; then
            log_success "Backup integrity verified"
        else
            log_warning "Could not verify backup format"
        fi
    fi
}

# Cleanup old backups
cleanup_old_backups() {
    log_info "Cleaning up backups older than $RETENTION_DAYS days..."

    local count=0

    # Find and delete old backup files
    while IFS= read -r -d '' file; do
        rm -f "$file"
        log_info "Deleted old backup: $(basename "$file")"
        count=$((count + 1))
    done < <(find "$BACKUP_DIR" -name "*.sql*" -type f -mtime +$RETENTION_DAYS -print0 2>/dev/null)

    if [ $count -gt 0 ]; then
        log_success "Cleaned up $count old backup(s)"
    else
        log_info "No old backups to clean up"
    fi
}

# List existing backups
list_backups() {
    log_info "Existing backups in $BACKUP_DIR:"
    echo ""

    if [ -d "$BACKUP_DIR" ]; then
        ls -lah "$BACKUP_DIR"/*.sql* 2>/dev/null || log_info "No backup files found"
    fi

    echo ""
}

# Show usage
show_usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -c, --compress     Enable compression (default: true)"
    echo "  -n, --no-compress  Disable compression"
    echo "  -l, --list         List existing backups"
    echo "  -r, --retention N  Set retention days (default: 7)"
    echo "  -h, --help         Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  BACKUP_DIR              Backup directory (default: ./backups)"
    echo "  MYSQL_DATABASE          Database name (default: msa_database)"
    echo "  MYSQL_ROOT_PASSWORD     MySQL root password (required)"
    echo "  BACKUP_RETENTION_DAYS   Days to keep backups (default: 7)"
    echo "  COMPRESS_BACKUP         Enable compression (default: true)"
    echo ""
}

# ================================
# Main
# ================================
main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -c|--compress)
                COMPRESS="true"
                shift
                ;;
            -n|--no-compress)
                COMPRESS="false"
                shift
                ;;
            -l|--list)
                list_backups
                exit 0
                ;;
            -r|--retention)
                RETENTION_DAYS="$2"
                shift 2
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    echo ""
    echo "================================"
    echo "  MSA Database Backup Script"
    echo "================================"
    echo ""

    # Update filename if compression changed
    if [ "$COMPRESS" = "true" ]; then
        FILENAME="${DB_NAME}_${TIMESTAMP}.sql.gz"
    else
        FILENAME="${DB_NAME}_${TIMESTAMP}.sql"
    fi
    BACKUP_PATH="${BACKUP_DIR}/${FILENAME}"

    # Ensure backup directory exists
    ensure_backup_dir

    # Find MySQL container
    log_info "Finding MySQL container..."
    CONTAINER_ID=$(find_mysql_container)
    log_success "Found MySQL container: $CONTAINER_ID"

    # Create backup
    create_backup "$CONTAINER_ID"

    # Verify backup
    verify_backup

    # Cleanup old backups
    cleanup_old_backups

    # Summary
    echo ""
    log_success "Backup completed successfully!"
    echo ""
    log_info "Backup location: $BACKUP_PATH"
    log_info "Retention policy: $RETENTION_DAYS days"
    echo ""
}

# Run main
main "$@"
