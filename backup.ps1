# ================================
# MSA Project Backup Script (PowerShell)
# ================================
# Backs up MySQL database with timestamp
# Supports: Windows 10/11
# ================================

$ErrorActionPreference = "Stop"

# ================================
# Emojis
# ================================
$CHECK = "✅"
$CROSS = "❌"
$DATABASE = "🗄️"
$SAVE = "💾"
$WARNING = "⚠️"

# ================================
# Helper Functions
# ================================
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$ForegroundColor = "White"
    )
    Write-Host $Message -ForegroundColor $ForegroundColor
}

# ================================
# Configuration
# ================================
$BackupDir = if ($env:BACKUP_DIR) { $env:BACKUP_DIR } else { ".\backups" }
$RetentionDays = if ($env:BACKUP_RETENTION_DAYS) { [int]$env:BACKUP_RETENTION_DAYS } else { 7 }
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$DbName = if ($env:MYSQL_DATABASE) { $env:MYSQL_DATABASE } else { "msa_database" }
$DbUser = if ($env:DB_USERNAME) { $env:DB_USERNAME } else { "root" }
$DbPass = if ($env:MYSQL_ROOT_PASSWORD) { $env:MYSQL_ROOT_PASSWORD } else { "defaultpassword123" }

# Determine container name
$ContainerName = $null
$containers = docker ps --format "{{.Names}}"

if ($containers -match "msa-mysql-dev") {
    $ContainerName = "msa-mysql-dev"
} elseif ($containers -match "msa-mysql-prod") {
    $ContainerName = "msa-mysql-prod"
} elseif ($containers -match "msa-mysql") {
    $ContainerName = "msa-mysql"
}

# ================================
# Banner
# ================================
Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-ColorOutput "║                                                            ║" -ForegroundColor Cyan
Write-ColorOutput "║         $DATABASE  MSA DATABASE BACKUP  $DATABASE                      ║" -ForegroundColor Cyan
Write-ColorOutput "║                                                            ║" -ForegroundColor Cyan
Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ================================
# Create Backup Directory
# ================================
Write-ColorOutput "[INFO] Creating backup directory..." -ForegroundColor Blue

if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

Write-ColorOutput "$CHECK Backup directory: " -ForegroundColor Green -NoNewline
Write-ColorOutput $BackupDir -ForegroundColor Cyan
Write-Host ""

# ================================
# Load Environment Variables
# ================================
if (Test-Path ".env") {
    Write-ColorOutput "[INFO] Loading environment variables from .env..." -ForegroundColor Blue
    
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^([^#].+?)=(.+)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            Set-Item -Path "env:$name" -Value $value
        }
    }
    
    # Update credentials if available
    $DbName = if ($env:MYSQL_DATABASE) { $env:MYSQL_DATABASE } else { $DbName }
    $DbUser = if ($env:DB_USERNAME) { $env:DB_USERNAME } else { $DbUser }
    $DbPass = if ($env:MYSQL_ROOT_PASSWORD) { $env:MYSQL_ROOT_PASSWORD } else { $DbPass }
    
    Write-ColorOutput "$CHECK Environment variables loaded" -ForegroundColor Green
} else {
    Write-ColorOutput "$WARNING .env file not found, using default values" -ForegroundColor Yellow
}
Write-Host ""

# ================================
# Check MySQL Container
# ================================
Write-ColorOutput "[INFO] Checking MySQL container status..." -ForegroundColor Blue

if (-not $ContainerName) {
    Write-ColorOutput "$CROSS MySQL container not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Available containers:"
    docker ps --format "table {{.Names}}`t{{.Status}}"
    exit 1
}

Write-ColorOutput "$CHECK MySQL container is running: " -ForegroundColor Green -NoNewline
Write-ColorOutput $ContainerName -ForegroundColor Cyan
Write-Host ""

# ================================
# Perform Backup
# ================================
$BackupFile = Join-Path $BackupDir "${DbName}_${Timestamp}.sql"

Write-ColorOutput "[INFO] Starting database backup..." -ForegroundColor Blue
Write-Host "Database: " -NoNewline
Write-ColorOutput $DbName -ForegroundColor Cyan
Write-Host "Container: " -NoNewline
Write-ColorOutput $ContainerName -ForegroundColor Cyan
Write-Host "Output: " -NoNewline
Write-ColorOutput $BackupFile -ForegroundColor Cyan
Write-Host ""

try {
    # Execute mysqldump inside container
    $dumpCmd = "mysqldump -u$DbUser -p$DbPass --single-transaction --routines --triggers --events $DbName"
    docker exec $ContainerName sh -c $dumpCmd | Out-File -FilePath $BackupFile -Encoding UTF8
    
    # Get file size
    $FileSize = (Get-Item $BackupFile).Length
    $FileSizeFormatted = if ($FileSize -gt 1MB) {
        "{0:N2} MB" -f ($FileSize / 1MB)
    } elseif ($FileSize -gt 1KB) {
        "{0:N2} KB" -f ($FileSize / 1KB)
    } else {
        "$FileSize bytes"
    }
    
    Write-ColorOutput "$CHECK Backup completed successfully!" -ForegroundColor Green
    Write-Host "File: " -NoNewline
    Write-ColorOutput $BackupFile -ForegroundColor Cyan
    Write-Host "Size: " -NoNewline
    Write-ColorOutput $FileSizeFormatted -ForegroundColor Cyan
} catch {
    Write-ColorOutput "$CROSS Backup failed!" -ForegroundColor Red
    Write-ColorOutput $_.Exception.Message -ForegroundColor Red
    if (Test-Path $BackupFile) {
        Remove-Item $BackupFile -Force
    }
    exit 1
}

Write-Host ""

# ================================
# Compress Backup (Optional)
# ================================
$compressChoice = Read-Host "Do you want to compress the backup? (y/N)"

if ($compressChoice -match "^[Yy]$") {
    Write-ColorOutput "[INFO] Compressing backup..." -ForegroundColor Blue
    
    try {
        Compress-Archive -Path $BackupFile -DestinationPath "$BackupFile.zip" -Force
        Remove-Item $BackupFile -Force
        $BackupFile = "$BackupFile.zip"
        
        $FileSize = (Get-Item $BackupFile).Length
        $FileSizeFormatted = if ($FileSize -gt 1MB) {
            "{0:N2} MB" -f ($FileSize / 1MB)
        } else {
            "{0:N2} KB" -f ($FileSize / 1KB)
        }
        
        Write-ColorOutput "$CHECK Backup compressed!" -ForegroundColor Green
        Write-Host "File: " -NoNewline
        Write-ColorOutput $BackupFile -ForegroundColor Cyan
        Write-Host "Size: " -NoNewline
        Write-ColorOutput $FileSizeFormatted -ForegroundColor Cyan
    } catch {
        Write-ColorOutput "$CROSS Compression failed!" -ForegroundColor Red
    }
    Write-Host ""
}

# ================================
# Clean Old Backups
# ================================
Write-ColorOutput "[INFO] Cleaning old backups (older than $RetentionDays days)..." -ForegroundColor Blue

$OldDate = (Get-Date).AddDays(-$RetentionDays)
$OldBackups = Get-ChildItem -Path $BackupDir -Filter "*.sql*" | Where-Object { $_.LastWriteTime -lt $OldDate }

if ($OldBackups) {
    foreach ($oldFile in $OldBackups) {
        Write-Host "   Removing: $($oldFile.Name)"
        Remove-Item $oldFile.FullName -Force
    }
    Write-ColorOutput "$CHECK Old backups cleaned" -ForegroundColor Green
} else {
    Write-Host "   No old backups to clean"
}

Write-Host ""

# ================================
# List Recent Backups
# ================================
Write-ColorOutput "[INFO] Recent backups:" -ForegroundColor Blue
Get-ChildItem -Path $BackupDir -Filter "*.sql*" | Sort-Object LastWriteTime -Descending | Select-Object -First 5 | ForEach-Object {
    $size = if ($_.Length -gt 1MB) { "{0:N2} MB" -f ($_.Length / 1MB) } else { "{0:N2} KB" -f ($_.Length / 1KB) }
    Write-Host "   $($_.Name) ($size)"
}
Write-Host ""

# ================================
# Summary
# ================================
Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-ColorOutput "║                                                            ║" -ForegroundColor Green
Write-ColorOutput "║         $SAVE  BACKUP COMPLETED SUCCESSFULLY  $SAVE                ║" -ForegroundColor Green
Write-ColorOutput "║                                                            ║" -ForegroundColor Green
Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Backup Details:"
Write-Host "   Database: $DbName"
Write-Host "   File: $BackupFile"
Write-Host "   Size: $FileSizeFormatted"
Write-Host "   Timestamp: $Timestamp"
Write-Host ""
Write-Host "🔧 Restore this backup:"
Write-Host "   .\scripts\restore.ps1 $BackupFile"
Write-Host ""
Write-Host "💡 Tips:"
Write-Host "   • Store backups in a secure location"
Write-Host "   • Test restore process regularly"
Write-Host "   • Keep backups for at least $RetentionDays days"
Write-Host ""
