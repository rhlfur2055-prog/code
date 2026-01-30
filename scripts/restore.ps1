# ================================
# MSA Project - Database Restore Script (PowerShell)
# ================================
# Restores MySQL database from backup file
# Usage: .\scripts\restore.ps1 -BackupFile <path>

param(
    [Parameter(Position=0)]
    [string]$BackupFile,

    [switch]$Help,
    [switch]$ListBackups,
    [switch]$Force
)

# ================================
# Configuration
# ================================
$BackupDir = ".\backups"
$ComposeFile = if ($env:COMPOSE_FILE) { $env:COMPOSE_FILE } else { "docker-compose.dev.yml" }

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
    Write-Host "Usage: .\scripts\restore.ps1 -BackupFile <path>" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Parameters:"
    Write-Host "  -BackupFile    Path to the backup file (.sql or .sql.gz)"
    Write-Host "  -ListBackups   List available backup files"
    Write-Host "  -Force         Skip confirmation prompt"
    Write-Host "  -Help          Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\scripts\restore.ps1 -BackupFile .\backups\msa_database_20240128_143022.sql"
    Write-Host "  .\scripts\restore.ps1 -ListBackups"
    Write-Host "  .\scripts\restore.ps1 -BackupFile .\backups\backup.sql -Force"
    Write-Host ""
}

function Get-BackupFiles {
    Write-Host ""
    Log-Info "Available backup files:"
    Write-Host ""

    if (Test-Path $BackupDir) {
        $files = Get-ChildItem -Path $BackupDir -Filter "*.sql*" -File | Sort-Object LastWriteTime -Descending

        if ($files.Count -eq 0) {
            Log-Warning "No backup files found in $BackupDir"
        } else {
            $index = 1
            foreach ($file in $files) {
                $size = "{0:N2} MB" -f ($file.Length / 1MB)
                $date = $file.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
                Write-Host "  $index. $($file.Name) ($size) - $date"
                $index++
            }
        }
    } else {
        Log-Error "Backup directory not found: $BackupDir"
    }
    Write-Host ""
}

function Find-MySqlContainer {
    $containerId = docker ps -qf "name=mysql" | Select-Object -First 1

    if (-not $containerId) {
        Log-Error "MySQL container not found. Is it running?"
        Log-Info "Start the services with: docker-compose -f $ComposeFile up -d"
        exit 1
    }

    return $containerId
}

function Test-BackupFile {
    param([string]$File)

    if (-not (Test-Path $File)) {
        Log-Error "Backup file not found: $File"
        exit 1
    }

    if ($File -notmatch '\.(sql|sql\.gz)$') {
        Log-Error "Invalid file format. Expected .sql or .sql.gz"
        exit 1
    }

    $fileInfo = Get-Item $File
    if ($fileInfo.Length -eq 0) {
        Log-Error "Backup file is empty: $File"
        exit 1
    }

    Log-Success "Backup file verified: $File"
}

function Restore-Database {
    param(
        [string]$BackupPath,
        [string]$ContainerId
    )

    # Load environment variables
    $envFile = ".\.env"
    $dbPassword = $null
    $dbName = "msa_database"

    if (Test-Path $envFile) {
        Get-Content $envFile | ForEach-Object {
            if ($_ -match "^MYSQL_ROOT_PASSWORD=(.*)") {
                $dbPassword = $matches[1]
            }
            if ($_ -match "^MYSQL_DATABASE=(.*)") {
                $dbName = $matches[1]
            }
        }
    }

    if (-not $dbPassword) {
        Log-Error "MYSQL_ROOT_PASSWORD not set. Please check your .env file."
        exit 1
    }

    Log-Info "Starting database restore..."
    Log-Warning "This will OVERWRITE the current database: $dbName"
    Write-Host ""

    # Confirmation
    if (-not $Force) {
        $confirm = Read-Host "Are you sure you want to continue? (yes/no)"
        if ($confirm -ne "yes") {
            Log-Info "Restore cancelled."
            exit 0
        }
    }

    Write-Host ""
    Log-Info "Restoring from: $BackupPath"

    try {
        # Check if compressed
        if ($BackupPath -match '\.gz$') {
            Log-Info "Decompressing and restoring backup file..."
            # For .gz files, we need 7-zip or gzip
            # Try using Docker to decompress
            $tempFile = [System.IO.Path]::GetTempFileName() + ".sql"

            # Check if gzip is available
            try {
                $content = & gzip -dc $BackupPath 2>$null
                $content | docker exec -i $ContainerId mysql -u root --password="$dbPassword" $dbName
            } catch {
                Log-Error "Failed to decompress .gz file. Please install gzip or use an uncompressed backup."
                exit 1
            }
        } else {
            Get-Content $BackupPath -Raw | docker exec -i $ContainerId mysql -u root --password="$dbPassword" $dbName
        }

        if ($LASTEXITCODE -eq 0) {
            Log-Success "Database restored successfully!"
        } else {
            throw "MySQL restore command failed"
        }
    } catch {
        Log-Error "Failed to restore database: $_"
        exit 1
    }
}

function Restart-Services {
    Log-Info "Restarting dependent services..."

    try {
        docker-compose -f $ComposeFile restart spring-api python-ai 2>$null
        Log-Success "Services restarted"
    } catch {
        Log-Warning "Could not restart services: $_"
    }
}

# ================================
# Main
# ================================
function Main {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "  MSA Database Restore Script" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""

    # Help
    if ($Help) {
        Show-Usage
        exit 0
    }

    # List backups
    if ($ListBackups -or (-not $BackupFile)) {
        Get-BackupFiles
        if (-not $BackupFile) {
            Write-Host "Usage: .\scripts\restore.ps1 -BackupFile <path>"
        }
        exit 0
    }

    # Verify backup file
    Test-BackupFile -File $BackupFile

    # Find MySQL container
    $containerId = Find-MySqlContainer
    Log-Info "Found MySQL container: $containerId"

    # Restore database
    Restore-Database -BackupPath $BackupFile -ContainerId $containerId

    # Ask to restart services
    Write-Host ""
    if (-not $Force) {
        $restart = Read-Host "Restart dependent services (spring-api, python-ai)? (y/N)"
        if ($restart -match "^[Yy]$") {
            Restart-Services
        }
    }

    Write-Host ""
    Log-Success "Restore process completed!"
    Write-Host ""
}

# Run main
Main
