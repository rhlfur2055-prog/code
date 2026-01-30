# ================================
# MSA Project Setup Script (PowerShell)
# ================================
# Automated setup for development and production environments
# Supports: Windows 10/11
# Author: MSA Project Team
# Version: 1.0.0
# ================================

# Error handling
$ErrorActionPreference = "Stop"

# ================================
# Color Codes
# ================================
function Write-ColorOutput {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        [string]$ForegroundColor = "White"
    )
    Write-Host $Message -ForegroundColor $ForegroundColor
}

# ================================
# Emojis
# ================================
$CHECK = "✅"
$CROSS = "❌"
$ROCKET = "🚀"
$GEAR = "⚙️"
$FOLDER = "📂"
$DATABASE = "🗄️"
$LOCK = "🔒"
$WARNING = "⚠️"

# ================================
# Banner
# ================================
function Show-Banner {
    Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-ColorOutput "║                                                            ║" -ForegroundColor Cyan
    Write-ColorOutput "║         $ROCKET  MSA PROJECT SETUP WIZARD  $ROCKET                  ║" -ForegroundColor Cyan
    Write-ColorOutput "║                                                            ║" -ForegroundColor Cyan
    Write-ColorOutput "║         Automated Deployment & Migration System            ║" -ForegroundColor Cyan
    Write-ColorOutput "║                                                            ║" -ForegroundColor Cyan
    Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

# ================================
# Logging Functions
# ================================
function Log-Info {
    param([string]$Message)
    Write-ColorOutput "[INFO] $Message" -ForegroundColor Blue
}

function Log-Success {
    param([string]$Message)
    Write-ColorOutput "$CHECK [SUCCESS] $Message" -ForegroundColor Green
}

function Log-Warning {
    param([string]$Message)
    Write-ColorOutput "$WARNING [WARNING] $Message" -ForegroundColor Yellow
}

function Log-Error {
    param([string]$Message)
    Write-ColorOutput "$CROSS [ERROR] $Message" -ForegroundColor Red
}

function Log-Step {
    param([string]$Message)
    Write-ColorOutput "$GEAR [STEP] $Message" -ForegroundColor Magenta
}

# ================================
# Prerequisites Check
# ================================
function Test-Prerequisites {
    Log-Step "Checking prerequisites..."
    
    $missingTools = @()
    
    # Check Docker
    try {
        $dockerVersion = docker --version 2>$null
        if ($dockerVersion) {
            Log-Success "Docker is installed ($dockerVersion)"
        } else {
            $missingTools += "Docker"
        }
    } catch {
        $missingTools += "Docker"
    }
    
    # Check Docker Compose
    try {
        $composeVersion = docker-compose --version 2>$null
        if ($composeVersion) {
            Log-Success "Docker Compose is installed ($composeVersion)"
        } else {
            $missingTools += "Docker Compose"
        }
    } catch {
        $missingTools += "Docker Compose"
    }
    
    # Report missing tools
    if ($missingTools.Count -gt 0) {
        Log-Error "Missing required tools: $($missingTools -join ', ')"
        Write-Host ""
        Write-Host "Please install the missing tools:"
        Write-Host "  - Docker Desktop: https://docs.docker.com/desktop/install/windows-install/"
        exit 1
    }
    
    Log-Success "All prerequisites satisfied!"
    Write-Host ""
}

# ================================
# Environment Selection
# ================================
function Select-Environment {
    Log-Step "Select deployment environment"
    Write-Host ""
    Write-Host "Available environments:"
    Write-ColorOutput "  1) Development (Hot reload, debug ports, verbose logging)" -ForegroundColor Cyan
    Write-ColorOutput "  2) Production (Optimized, secure, resource-limited)" -ForegroundColor Cyan
    Write-Host ""
    
    do {
        $envChoice = Read-Host "Enter your choice (1 or 2)"
        
        switch ($envChoice) {
            "1" {
                $script:Environment = "dev"
                $script:ComposeFile = "docker-compose.dev.yml"
                Log-Success "Development environment selected"
                $valid = $true
            }
            "2" {
                $script:Environment = "prod"
                $script:ComposeFile = "docker-compose.prod.yml"
                Log-Success "Production environment selected"
                $valid = $true
            }
            default {
                Log-Error "Invalid choice. Please enter 1 or 2."
                $valid = $false
            }
        }
    } while (-not $valid)
    
    Write-Host ""
}

# ================================
# Environment File Setup
# ================================
function Setup-EnvFile {
    Log-Step "Setting up environment variables..."
    
    if (Test-Path ".env") {
        Log-Warning ".env file already exists"
        $overwrite = Read-Host "Do you want to overwrite it? (y/N)"
        if ($overwrite -notmatch "^[Yy]$") {
            Log-Info "Using existing .env file"
            return
        }
    }
    
    if (-not (Test-Path ".env.example")) {
        Log-Error ".env.example not found!"
        exit 1
    }
    
    Log-Info "Copying .env.example to .env..."
    Copy-Item ".env.example" ".env"
    
    # Interactive configuration
    Write-Host ""
    Log-Info "Let's configure your environment variables..."
    Write-Host ""
    
    # Database password
    $mysqlPassword = Read-Host "Enter MySQL root password" -AsSecureString
    $mysqlPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($mysqlPassword)
    )
    
    if ([string]::IsNullOrEmpty($mysqlPasswordPlain)) {
        $mysqlPasswordPlain = "defaultpassword123"
        Log-Warning "Using default password (CHANGE THIS IN PRODUCTION!)"
    }
    
    (Get-Content ".env") -replace "your_mysql_password_here", $mysqlPasswordPlain | Set-Content ".env"
    
    # JWT Secret
    $jwtSecret = Read-Host "Enter JWT secret (press Enter for auto-generation)"
    if ([string]::IsNullOrEmpty($jwtSecret)) {
        $jwtSecret = "autogenerated_jwt_secret_$((Get-Date).Ticks)"
        Log-Info "JWT secret auto-generated"
    }
    
    (Get-Content ".env") -replace "your_jwt_secret_key_change_this_in_production", $jwtSecret | Set-Content ".env"
    
    # Set environment
    if ($script:Environment -eq "prod") {
        (Get-Content ".env") -replace "NODE_ENV=development", "NODE_ENV=production" | Set-Content ".env"
        (Get-Content ".env") -replace "SPRING_PROFILE=dev", "SPRING_PROFILE=prod" | Set-Content ".env"
        (Get-Content ".env") -replace "FASTAPI_ENV=development", "FASTAPI_ENV=production" | Set-Content ".env"
    }
    
    Log-Success "Environment file configured!"
    Write-Host ""
}

# ================================
# Docker Build
# ================================
function Build-DockerImages {
    Log-Step "Building Docker images..."
    Write-Host ""
    
    Log-Info "This may take several minutes on first run..."
    Write-Host ""
    
    try {
        docker-compose -f $script:ComposeFile build --no-cache
        Log-Success "Docker images built successfully!"
    } catch {
        Log-Error "Failed to build Docker images"
        Log-Error $_.Exception.Message
        exit 1
    }
    
    Write-Host ""
}

# ================================
# Start Services
# ================================
function Start-Services {
    Log-Step "Starting services..."
    Write-Host ""
    
    try {
        docker-compose -f $script:ComposeFile up -d
        Log-Success "Services started successfully!"
    } catch {
        Log-Error "Failed to start services"
        Log-Error $_.Exception.Message
        exit 1
    }
    
    Write-Host ""
}

# ================================
# Health Check
# ================================
function Test-ServicesHealth {
    Log-Step "Running health checks..."
    Write-Host ""
    
    Log-Info "Waiting for services to be ready (this may take 1-2 minutes)..."
    Start-Sleep -Seconds 10
    
    # Check each service
    $services = @(
        @{Name="frontend"; Endpoint="http://localhost:3000"},
        @{Name="spring-api"; Endpoint="http://localhost:8080/actuator/health"},
        @{Name="python-ai"; Endpoint="http://localhost:8000/health"}
    )
    
    foreach ($service in $services) {
        Write-Host "Checking " -NoNewline
        Write-ColorOutput $service.Name -ForegroundColor Cyan -NoNewline
        Write-Host "... " -NoNewline
        
        $maxRetries = 30
        $retryCount = 0
        $healthy = $false
        
        while ($retryCount -lt $maxRetries) {
            try {
                $response = Invoke-WebRequest -Uri $service.Endpoint -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
                if ($response.StatusCode -eq 200) {
                    Write-ColorOutput "$CHECK Healthy" -ForegroundColor Green
                    $healthy = $true
                    break
                }
            } catch {
                # Continue retrying
            }
            
            $retryCount++
            Start-Sleep -Seconds 2
        }
        
        if (-not $healthy) {
            Write-ColorOutput "$CROSS Unhealthy" -ForegroundColor Red
            Log-Warning "$($service.Name) is not responding. Check logs: docker-compose -f $($script:ComposeFile) logs $($service.Name)"
        }
    }
    
    Write-Host ""
}

# ================================
# Display Summary
# ================================
function Show-Summary {
    Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-ColorOutput "║                                                            ║" -ForegroundColor Cyan
    Write-ColorOutput "║                  $ROCKET SETUP COMPLETE! $ROCKET                       ║" -ForegroundColor Cyan
    Write-ColorOutput "║                                                            ║" -ForegroundColor Cyan
    Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    
    Log-Success "MSA Project is now running!"
    Write-Host ""
    Write-Host "📍 Service URLs:"
    Write-ColorOutput "   Frontend:     http://localhost:3000" -ForegroundColor Cyan
    Write-ColorOutput "   Spring API:   http://localhost:8080" -ForegroundColor Cyan
    Write-ColorOutput "   Python AI:    http://localhost:8000" -ForegroundColor Cyan
    if ($script:Environment -eq "dev") {
        Write-ColorOutput "   phpMyAdmin:   http://localhost:8081" -ForegroundColor Cyan
    }
    Write-Host ""
    
    Write-Host "📋 Useful commands:"
    Write-ColorOutput "   View logs:        docker-compose -f $($script:ComposeFile) logs -f" -ForegroundColor Yellow
    Write-ColorOutput "   Stop services:    docker-compose -f $($script:ComposeFile) down" -ForegroundColor Yellow
    Write-ColorOutput "   Restart:          docker-compose -f $($script:ComposeFile) restart" -ForegroundColor Yellow
    Write-ColorOutput "   Health check:     .\scripts\healthcheck.ps1" -ForegroundColor Yellow
    Write-ColorOutput "   Backup DB:        .\scripts\backup.ps1" -ForegroundColor Yellow
    Write-Host ""
    
    if ($script:Environment -eq "prod") {
        Write-ColorOutput "$WARNING  PRODUCTION REMINDERS:" -ForegroundColor Yellow
        Write-Host "   - Ensure firewall is configured"
        Write-Host "   - Set up SSL certificates"
        Write-Host "   - Configure regular backups"
        Write-Host "   - Monitor resource usage"
        Write-Host ""
    }
}

# ================================
# Cleanup on Error
# ================================
function Cleanup-OnError {
    Log-Error "Setup failed. Cleaning up..."
    try {
        docker-compose -f $script:ComposeFile down 2>$null
    } catch {
        # Ignore cleanup errors
    }
    exit 1
}

# ================================
# Main Execution
# ================================
function Main {
    try {
        # Clear screen
        Clear-Host
        
        # Show banner
        Show-Banner
        
        # Check prerequisites
        Test-Prerequisites
        
        # Select environment
        Select-Environment
        
        # Setup .env file
        Setup-EnvFile
        
        # Build images
        $buildChoice = Read-Host "Do you want to build Docker images? (Y/n)"
        if ($buildChoice -notmatch "^[Nn]$") {
            Build-DockerImages
        }
        
        # Start services
        Start-Services
        
        # Run health checks
        Test-ServicesHealth
        
        # Display summary
        Show-Summary
        
        Log-Success "Setup script completed successfully! $ROCKET"
    } catch {
        Cleanup-OnError
    }
}

# Run main function
Main
