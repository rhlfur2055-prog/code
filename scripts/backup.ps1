# ================================
# MSA Project - Enhanced Database Backup Script (PowerShell)
# ================================
# Features:
# - Timestamped backups
# - Optional compression (gzip)
# - Automatic cleanup of old backups
# - Integrity verification
# - Configurable retention period

param(
    [switch]$Compress,
    [switch]$NoCompress,
    [switch]$List,
    [int]$Retention = 7,
    [switch]$Help
)

# ================================
# Configuration
# ================================
$BackupDir = if ($env:BACKUP_DIR) { $env:BACKUP_DIR } else { ".\backups" }
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$DbName = if ($env:MYSQL_DATABASE) { $env:MYSQL_DATABASE } else { "msa_database" }
$RetentionDays = if ($env:BACKUP_RETENTION_DAYS) { [int]$env:BACKUP_RETENTION_DAYS } else { $Retention }
$EnableCompress = if ($NoCompress) { $false } elseif ($Compress) { $true } else { $true }

# Load .env file
if (Test-Path ".\.env") {
    Get-Content ".\.env" | ForEach-Object {
        if ($_ -match "^([^#][^=]+)=(.*)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
}

# Filename
$Extension = if ($EnableCompress) { ".sql.gz" } else { ".sql" }
$Filename = "${DbName}_${Timestamp}${Extension}"
$BackupPath = Join-Path $BackupDir $Filename

# ================================
# Functions
# ================================
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Log-Info {
    param([string]$Message)
    Write-ColorOutput "[INFO] $Message" -Color Blue
}

function Log-Success {
    param([string]$Message)
    Write-ColorOutput "[SUCCESS] $Message" -Color Green
}

function Log-Warning {
    param([string]$Message)
    Write-ColorOutput "[WARNING] $Message" -Color Yellow
}

function Log-Error {
    param([string]$Message)
    Write-ColorOutput "[ERROR] $Message" -Color Red
}

function Show-Usage {
    Write-Host ""
    Write-Host "Usage: .\scripts\backup.ps1 [options]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Compress       Enable compression (default: true)"
    Write-Host "  -NoCompress     Disable compression"
    Write-Host "  -List           List existing backups"
    Write-Host "  -Retention N    Set retention days (default: 7)"
    Write-Host "  -Help           Show this help message"
    Write-Host ""
    Write-Host "Environment variables:"
    Write-Host "  BACKUP_DIR              Backup directory (default: .\backups)"
    Write-Host "  MYSQL_DATABASE          Database name (default: msa_database)"
    Write-Host "  MYSQL_ROOT_PASSWORD     MySQL root password (required)"
    Write-Host "  BACKUP_RETENTION_DAYS   Days to keep backups (default: 7)"
    Write-Host ""
}

function Ensure-BackupDir {
    if (-not (Test-Path $BackupDir)) {
        Log-Info "Creating backup directory: $BackupDir"
        New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
    }
}

function Find-MySqlContainer {
    $containerId = docker ps -qf "name=mysql" | Select-Object -First 1

    if (-not $containerId) {
        Log-Error "MySQL container not found. Is it running?"
        Log-Info "Start the services first: docker-compose up -d"
        exit 1
    }

    return $containerId
}

function Create-Backup {
    param([string]$ContainerId)

    $dbPassword = $env:MYSQL_ROOT_PASSWORD

    if (-not $dbPassword) {
        Log-Error "MYSQL_ROOT_PASSWORD not set. Please check your .env file."
        exit 1
    }

    Log-Info "Creating backup of database: $DbName"
    Log-Info "Backup file: $BackupPath"

    try {
        if ($EnableCompress) {
            Log-Info "Compression enabled"
            # Note: PowerShell doesn't have native gzip, so we'll save uncompressed
            # and compress separately if 7-zip is available
            $tempFile = [System.IO.Path]::GetTempFileName()

            docker exec $ContainerId /usr/bin/mysqldump `
                -u root `
                --password="$dbPassword" `
                --single-transaction `
                --routines `
                --triggers `
                --databases $DbName | Out-File -FilePath $tempFile -Encoding utf8

            # Try to compress with gzip if available in WSL/Docker
            try {
                docker run --rm -v "${PWD}:/data" alpine sh -c "gzip -c /data/$($tempFile | Split-Path -Leaf) > /data/$Filename"
                Remove-Item $tempFile -ErrorAction SilentlyContinue
            } catch {
                # Fall back to uncompressed
                $BackupPath = $BackupPath -replace '\.gz$', ''
                Move-Item $tempFile $BackupPath
                Log-Warning "Compression not available, saved uncompressed"
            }
        } else {
            docker exec $ContainerId /usr/bin/mysqldump `
                -u root `
                --password="$dbPassword" `
                --single-transaction `
                --routines `
                --triggers `
                --databases $DbName | Out-File -FilePath $BackupPath -Encoding utf8
        }

        if (Test-Path $BackupPath) {
            $size = "{0:N2} MB" -f ((Get-Item $BackupPath).Length / 1MB)
            Log-Success "Backup created successfully: $BackupPath ($size)"
        } else {
            throw "Backup file not created"
        }
    } catch {
        Log-Error "Backup failed: $_"
        Remove-Item $BackupPath -ErrorAction SilentlyContinue
        exit 1
    }
}

function Verify-Backup {
    Log-Info "Verifying backup integrity..."

    if (-not (Test-Path $BackupPath)) {
        Log-Error "Backup file not found!"
        exit 1
    }

    $file = Get-Item $BackupPath

    if ($file.Length -lt 100) {
        Log-Error "Backup file is too small (possibly corrupted)"
        exit 1
    }

    # Check file content
    $firstLine = Get-Content $BackupPath -First 1 -ErrorAction SilentlyContinue
    if ($firstLine -match "MySQL|mysqldump|--") {
        Log-Success "Backup integrity verified"
    } else {
        Log-Warning "Could not verify backup format"
    }
}

function Cleanup-OldBackups {
    Log-Info "Cleaning up backups older than $RetentionDays days..."

    $cutoffDate = (Get-Date).AddDays(-$RetentionDays)
    $oldFiles = Get-ChildItem -Path $BackupDir -Filter "*.sql*" -File |
                Where-Object { $_.LastWriteTime -lt $cutoffDate }

    $count = 0
    foreach ($file in $oldFiles) {
        Remove-Item $file.FullName -Force
        Log-Info "Deleted old backup: $($file.Name)"
        $count++
    }

    if ($count -gt 0) {
        Log-Success "Cleaned up $count old backup(s)"
    } else {
        Log-Info "No old backups to clean up"
    }
}

function Get-BackupList {
    Log-Info "Existing backups in $BackupDir`:"
    Write-Host ""

    if (Test-Path $BackupDir) {
        $files = Get-ChildItem -Path $BackupDir -Filter "*.sql*" -File | Sort-Object LastWriteTime -Descending

        if ($files.Count -eq 0) {
            Log-Info "No backup files found"
        } else {
            foreach ($file in $files) {
                $size = "{0:N2} MB" -f ($file.Length / 1MB)
                $date = $file.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
                Write-Host "  $($file.Name) ($size) - $date"
            }
        }
    } else {
        Log-Info "Backup directory does not exist"
    }

    Write-Host ""
}

# ================================
# Main
# ================================
function Main {
    if ($Help) {
        Show-Usage
        exit 0
    }

    if ($List) {
        Get-BackupList
        exit 0
    }

    Write-Host ""
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "  MSA Database Backup Script" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""

    # Ensure backup directory exists
    Ensure-BackupDir

    # Find MySQL container
    Log-Info "Finding MySQL container..."
    $containerId = Find-MySqlContainer
    Log-Success "Found MySQL container: $containerId"

    # Create backup
    Create-Backup -ContainerId $containerId

    # Verify backup
    Verify-Backup

    # Cleanup old backups
    Cleanup-OldBackups

    # Summary
    Write-Host ""
    Log-Success "Backup completed successfully!"
    Write-Host ""
    Log-Info "Backup location: $BackupPath"
    Log-Info "Retention policy: $RetentionDays days"
    Write-Host ""
}

# Run main
Main
