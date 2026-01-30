#!/bin/bash

# ================================
# MSA Project Backup Script
# ================================
# Backs up MySQL database with timestamp
# Supports: Linux, macOS, WSL
# ================================

set -e

# ================================
# Color Codes
# ================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Emojis
CHECK="✅"
CROSS="❌"
DATABASE="🗄️"
SAVE="💾"
WARNING="⚠️"

# ================================
# Configuration
# ================================
BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="${MYSQL_DATABASE:-msa_database}"
DB_USER="${DB_USERNAME:-root}"
DB_PASS="${MYSQL_ROOT_PASSWORD:-defaultpassword123}"

# Determine environment
if [ -f "docker-compose.dev.yml" ] && docker-compose -f docker-compose.dev.yml ps | grep -q "mysql"; then
    CONTAINER_NAME="msa-mysql-dev"
elif [ -f "docker-compose.prod.yml" ] && docker-compose -f docker-compose.prod.yml ps | grep -q "mysql"; then
    CONTAINER_NAME="msa-mysql-prod"
else
    CONTAINER_NAME="msa-mysql"
fi

# ================================
# Banner
# ================================
echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║         ${DATABASE}  MSA DATABASE BACKUP  ${DATABASE}                      ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# ================================
# Create Backup Directory
# ================================
echo -e "${BLUE}[INFO]${NC} Creating backup directory..."
mkdir -p "$BACKUP_DIR"
echo -e "${GREEN}${CHECK}${NC} Backup directory: ${CYAN}${BACKUP_DIR}${NC}"
echo ""

# ================================
# Load Environment Variables
# ================================
if [ -f ".env" ]; then
    echo -e "${BLUE}[INFO]${NC} Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
    
    # Update credentials if available
    DB_NAME="${MYSQL_DATABASE:-$DB_NAME}"
    DB_USER="${DB_USERNAME:-$DB_USER}"
    DB_PASS="${MYSQL_ROOT_PASSWORD:-$DB_PASS}"
    
    echo -e "${GREEN}${CHECK}${NC} Environment variables loaded"
else
    echo -e "${YELLOW}${WARNING}${NC} .env file not found, using default values"
fi
echo ""

# ================================
# Check MySQL Container
# ================================
echo -e "${BLUE}[INFO]${NC} Checking MySQL container status..."

if ! docker ps --format '{{.Names}}' | grep -q "$CONTAINER_NAME"; then
    echo -e "${RED}${CROSS}${NC} MySQL container '${CONTAINER_NAME}' is not running!"
    echo ""
    echo "Available containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}"
    exit 1
fi

echo -e "${GREEN}${CHECK}${NC} MySQL container is running: ${CYAN}${CONTAINER_NAME}${NC}"
echo ""

# ================================
# Perform Backup
# ================================
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql"

echo -e "${BLUE}[INFO]${NC} Starting database backup..."
echo "Database: ${CYAN}${DB_NAME}${NC}"
echo "Container: ${CYAN}${CONTAINER_NAME}${NC}"
echo "Output: ${CYAN}${BACKUP_FILE}${NC}"
echo ""

# Execute mysqldump inside container
if docker exec "$CONTAINER_NAME" mysqldump \
    -u"${DB_USER}" \
    -p"${DB_PASS}" \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    "${DB_NAME}" > "$BACKUP_FILE" 2>/dev/null; then
    
    # Get file size
    FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    
    echo -e "${GREEN}${CHECK}${NC} Backup completed successfully!"
    echo "File: ${CYAN}${BACKUP_FILE}${NC}"
    echo "Size: ${CYAN}${FILE_SIZE}${NC}"
else
    echo -e "${RED}${CROSS}${NC} Backup failed!"
    rm -f "$BACKUP_FILE"
    exit 1
fi

echo ""

# ================================
# Compress Backup (Optional)
# ================================
read -p "Do you want to compress the backup? (y/N): " compress_choice

if [[ $compress_choice =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}[INFO]${NC} Compressing backup..."
    
    if gzip "$BACKUP_FILE"; then
        BACKUP_FILE="${BACKUP_FILE}.gz"
        FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
        
        echo -e "${GREEN}${CHECK}${NC} Backup compressed!"
        echo "File: ${CYAN}${BACKUP_FILE}${NC}"
        echo "Size: ${CYAN}${FILE_SIZE}${NC}"
    else
        echo -e "${RED}${CROSS}${NC} Compression failed!"
    fi
    echo ""
fi

# ================================
# Clean Old Backups
# ================================
echo -e "${BLUE}[INFO]${NC} Cleaning old backups (older than ${RETENTION_DAYS} days)..."

OLD_BACKUPS=$(find "$BACKUP_DIR" -name "*.sql*" -type f -mtime +${RETENTION_DAYS} 2>/dev/null)

if [ -n "$OLD_BACKUPS" ]; then
    echo "$OLD_BACKUPS" | while read -r old_file; do
        echo "   Removing: $(basename "$old_file")"
        rm -f "$old_file"
    done
    echo -e "${GREEN}${CHECK}${NC} Old backups cleaned"
else
    echo "   No old backups to clean"
fi

echo ""

# ================================
# List Recent Backups
# ================================
echo -e "${BLUE}[INFO]${NC} Recent backups:"
ls -lh "$BACKUP_DIR"/*.sql* 2>/dev/null | tail -5 | awk '{print "   " $9 " (" $5 ")"}'
echo ""

# ================================
# Backup Verification
# ================================
echo -e "${BLUE}[INFO]${NC} Verifying backup integrity..."

if [[ "$BACKUP_FILE" == *.gz ]]; then
    if gzip -t "$BACKUP_FILE" 2>/dev/null; then
        echo -e "${GREEN}${CHECK}${NC} Backup file is valid and intact"
    else
        echo -e "${RED}${CROSS}${NC} Backup file may be corrupted!"
        exit 1
    fi
else
    if grep -q "Dump completed" "$BACKUP_FILE" 2>/dev/null; then
        echo -e "${GREEN}${CHECK}${NC} Backup file is valid and intact"
    else
        echo -e "${YELLOW}${WARNING}${NC} Backup file verification inconclusive"
    fi
fi

echo ""

# ================================
# Summary
# ================================
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║         ${SAVE}  BACKUP COMPLETED SUCCESSFULLY  ${SAVE}                ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo "📋 Backup Details:"
echo "   Database: ${DB_NAME}"
echo "   File: ${BACKUP_FILE}"
echo "   Size: ${FILE_SIZE}"
echo "   Timestamp: ${TIMESTAMP}"
echo ""
echo "🔧 Restore this backup:"
echo "   ./scripts/restore.sh ${BACKUP_FILE}"
echo ""
echo "💡 Tips:"
echo "   • Store backups in a secure location"
echo "   • Test restore process regularly"
echo "   • Keep backups for at least ${RETENTION_DAYS} days"
echo ""
