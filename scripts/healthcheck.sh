#!/bin/bash

# scripts/healthcheck.sh - Service Health Check

echo "Checking K-MaaS Service Health..."

# Function to check URL
check_url() {
    local NAME=$1
    local URL=$2
    
    if curl --output /dev/null --silent --head --fail "$URL"; then
        echo -e "[\033[0;32mOK\033[0m] $NAME is running ($URL)"
    else
        echo -e "[\033[0;31mFAIL\033[0m] $NAME is NOT accessible ($URL)"
    fi
}

# Function to check Port (using nc)
check_port() {
    local NAME=$1
    local HOST=$2
    local PORT=$3
    
    nc -z -w 2 "$HOST" "$PORT" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "[\033[0;32mOK\033[0m] $NAME port $PORT is open"
    else
        echo -e "[\033[0;31mFAIL\033[0m] $NAME port $PORT is CLOSED"
    fi
}

# Check Services
# Note: In a docker network, use container names. From host, use localhost.
echo "--- Endpoint Checks (Host) ---"
check_url "Frontend" "http://localhost:3000"
check_url "Spring API" "http://localhost:8080/actuator/health"
check_url "AI Server" "http://localhost:8000/health"

echo ""
echo "--- DB Port Checks ---"
# Assuming ports are exposed to host
check_port "MySQL" "localhost" "3306"
check_port "Redis" "localhost" "6379"

echo ""
echo "Done."
