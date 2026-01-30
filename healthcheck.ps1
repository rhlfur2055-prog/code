# ================================
# MSA Project Health Check Script (PowerShell)
# ================================
# Verifies all services are running correctly
# Supports: Windows 10/11
# ================================

$ErrorActionPreference = "Continue"

# ================================
# Emojis
# ================================
$CHECK = "✅"
$CROSS = "❌"
$HEART = "❤️"
$WARNING = "⚠️"

# ================================
# Configuration
# ================================
$Services = @(
    @{Name="Frontend (Next.js)"; Endpoint="http://localhost:3000"},
    @{Name="Spring Boot API"; Endpoint="http://localhost:8080/actuator/health"},
    @{Name="Python AI Server"; Endpoint="http://localhost:8000/health"},
    @{Name="MySQL Database"; Endpoint="localhost:3306"; Type="TCP"}
)

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
# Banner
# ================================
Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-ColorOutput "║                                                            ║" -ForegroundColor Cyan
Write-ColorOutput "║         $HEART  MSA PROJECT HEALTH CHECK  $HEART                    ║" -ForegroundColor Cyan
Write-ColorOutput "║                                                            ║" -ForegroundColor Cyan
Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ================================
# Check Docker Services
# ================================
Write-ColorOutput "[INFO] Checking Docker services status..." -ForegroundColor Blue
Write-Host ""

# Determine which compose file to use
$ComposeFile = "docker-compose.yml"
if (Test-Path "docker-compose.dev.yml") {
    try {
        $devStatus = docker-compose -f docker-compose.dev.yml ps 2>$null
        if ($devStatus -match "Up") {
            $ComposeFile = "docker-compose.dev.yml"
        }
    } catch {}
}
if (Test-Path "docker-compose.prod.yml" -and $ComposeFile -eq "docker-compose.yml") {
    try {
        $prodStatus = docker-compose -f docker-compose.prod.yml ps 2>$null
        if ($prodStatus -match "Up") {
            $ComposeFile = "docker-compose.prod.yml"
        }
    } catch {}
}

Write-Host "Using compose file: " -NoNewline
Write-ColorOutput $ComposeFile -ForegroundColor Cyan
Write-Host ""

# Container status
try {
    $containers = docker-compose -f $ComposeFile ps --services 2>$null
    
    if (-not $containers) {
        Write-ColorOutput "$CROSS No running containers found!" -ForegroundColor Red
        Write-Host "Run '.\setup.ps1' to start the services."
        exit 1
    }
    
    Write-Host "📦 Container Status:"
    foreach ($container in $containers) {
        $status = docker-compose -f $ComposeFile ps $container 2>$null | Select-String $container
        
        if ($status -match "Up|running") {
            Write-Host "   " -NoNewline
            Write-ColorOutput "$CHECK" -ForegroundColor Green -NoNewline
            Write-Host " ${container}: " -NoNewline
            Write-ColorOutput "Running" -ForegroundColor Green
        } else {
            Write-Host "   " -NoNewline
            Write-ColorOutput "$CROSS" -ForegroundColor Red -NoNewline
            Write-Host " ${container}: " -NoNewline
            Write-ColorOutput "Stopped" -ForegroundColor Red
        }
    }
} catch {
    Write-ColorOutput "$CROSS Error checking container status" -ForegroundColor Red
}

Write-Host ""

# ================================
# Health Checks
# ================================
Write-ColorOutput "[INFO] Running health checks..." -ForegroundColor Blue
Write-Host ""

$allHealthy = $true

foreach ($service in $Services) {
    Write-Host "Testing " -NoNewline
    Write-ColorOutput $service.Name -ForegroundColor Cyan -NoNewline
    Write-Host "... " -NoNewline
    
    # MySQL special handling
    if ($service.Type -eq "TCP") {
        try {
            $tcpClient = New-Object System.Net.Sockets.TcpClient
            $tcpClient.Connect("localhost", 3306)
            $tcpClient.Close()
            Write-ColorOutput "$CHECK Healthy (TCP)" -ForegroundColor Green
        } catch {
            Write-ColorOutput "$CROSS Unhealthy" -ForegroundColor Red
            $allHealthy = $false
        }
        continue
    }
    
    # HTTP health check
    try {
        $response = Invoke-WebRequest -Uri $service.Endpoint -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-ColorOutput "$CHECK Healthy (HTTP $($response.StatusCode))" -ForegroundColor Green
        } else {
            Write-ColorOutput "$WARNING Degraded (HTTP $($response.StatusCode))" -ForegroundColor Yellow
            $allHealthy = $false
        }
    } catch {
        Write-ColorOutput "$CROSS Unreachable" -ForegroundColor Red
        $allHealthy = $false
    }
}

Write-Host ""

# ================================
# Resource Usage
# ================================
Write-ColorOutput "[INFO] Resource usage:" -ForegroundColor Blue
Write-Host ""

try {
    docker stats --no-stream --format "table {{.Name}}`t{{.CPUPerc}}`t{{.MemUsage}}" | Select-String -Pattern "CONTAINER|msa-" | Select-Object -First 10
} catch {
    Write-ColorOutput "Unable to fetch resource usage" -ForegroundColor Yellow
}

Write-Host ""

# ================================
# Summary
# ================================
if ($allHealthy) {
    Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-ColorOutput "║                                                            ║" -ForegroundColor Green
    Write-ColorOutput "║         $CHECK  ALL SERVICES ARE HEALTHY  $CHECK                    ║" -ForegroundColor Green
    Write-ColorOutput "║                                                            ║" -ForegroundColor Green
    Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Access your services:"
    Write-Host "   • Frontend:   http://localhost:3000"
    Write-Host "   • Spring API: http://localhost:8080"
    Write-Host "   • Python AI:  http://localhost:8000"
    Write-Host ""
    exit 0
} else {
    Write-ColorOutput "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-ColorOutput "║                                                            ║" -ForegroundColor Yellow
    Write-ColorOutput "║         $WARNING  SOME SERVICES ARE UNHEALTHY  $WARNING                ║" -ForegroundColor Yellow
    Write-ColorOutput "║                                                            ║" -ForegroundColor Yellow
    Write-ColorOutput "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🔍 Troubleshooting steps:"
    Write-Host "   1. Check logs: docker-compose -f $ComposeFile logs -f"
    Write-Host "   2. Restart services: docker-compose -f $ComposeFile restart"
    Write-Host "   3. Rebuild: docker-compose -f $ComposeFile up -d --build"
    Write-Host ""
    exit 1
}
