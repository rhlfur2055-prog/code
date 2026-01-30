# scripts/healthcheck.ps1 - Service Health Check

Write-Output "Checking K-MaaS Service Health..."

function Check-Url {
    param (
        [string]$Name,
        [string]$Url
    )
    try {
        $response = Invoke-WebRequest -Uri $Url -Method Head -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "[$([char]0x2713) OK] $Name is running ($Url)" -ForegroundColor Green
        } else {
            Write-Host "[FAIL] $Name returned status $($response.StatusCode)" -ForegroundColor Red
        }
    } catch {
        Write-Host "[FAIL] $Name is NOT accessible ($Url)" -ForegroundColor Red
    }
}

function Check-Port {
    param (
        [string]$Name,
        [string]$HostName,
        [int]$Port
    )
    try {
        $tcp = New-Object Net.Sockets.TcpClient
        $connect = $tcp.BeginConnect($HostName, $Port, $null, $null)
        $wait = $connect.AsyncWaitHandle.WaitOne(2000, $false)
        if ($wait -and $tcp.Connected) {
             Write-Host "[$([char]0x2713) OK] $Name port $Port is open" -ForegroundColor Green
             $tcp.EndConnect($connect)
             $tcp.Close()
        } else {
             Write-Host "[FAIL] $Name port $Port is CLOSED" -ForegroundColor Red
        }
    } catch {
         Write-Host "[FAIL] Error checking $Name port $Port" -ForegroundColor Red
    }
}

# Check Services
Write-Host "--- Endpoint Checks (Host) ---"
Check-Url -Name "Frontend" -Url "http://localhost:3000"
Check-Url -Name "Spring API" -Url "http://localhost:8080/actuator/health"
Check-Url -Name "AI Server" -Url "http://localhost:8000/health"

Write-Host ""
Write-Host "--- DB Port Checks ---"
Check-Port -Name "MySQL" -HostName "localhost" -Port 3306
Check-Port -Name "Redis" -HostName "localhost" -Port 6379

Write-Host ""
Write-Host "Done."
