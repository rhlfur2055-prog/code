#!/bin/bash

# ================================
# MSA Project Health Check Script
# ================================
# Verifies all services are running correctly
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
HEART="❤️"
WARNING="⚠️"

# ================================
# Configuration
# ================================
SERVICES=(
    "frontend|http://localhost:3000|Frontend (Next.js)"
    "spring-api|http://localhost:8080/actuator/health|Spring Boot API"
    "python-ai|http://localhost:8000/health|Python AI Server"
    "mysql|localhost:3306|MySQL Database"
)

# ================================
# Banner
# ================================
echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║         ${HEART}  MSA PROJECT HEALTH CHECK  ${HEART}                    ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# ================================
# Check Docker Services
# ================================
echo -e "${BLUE}[INFO]${NC} Checking Docker services status..."
echo ""

# Determine which compose file to use
if [ -f "docker-compose.dev.yml" ] && docker-compose -f docker-compose.dev.yml ps | grep -q "Up"; then
    COMPOSE_FILE="docker-compose.dev.yml"
elif [ -f "docker-compose.prod.yml" ] && docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    COMPOSE_FILE="docker-compose.prod.yml"
else
    COMPOSE_FILE="docker-compose.yml"
fi

echo "Using compose file: ${CYAN}${COMPOSE_FILE}${NC}"
echo ""

# Container status
containers=$(docker-compose -f "$COMPOSE_FILE" ps --services 2>/dev/null)

if [ -z "$containers" ]; then
    echo -e "${RED}${CROSS} No running containers found!${NC}"
    echo "Run './setup.sh' to start the services."
    exit 1
fi

echo "📦 Container Status:"
while IFS= read -r container; do
    status=$(docker-compose -f "$COMPOSE_FILE" ps "$container" 2>/dev/null | grep "$container" | awk '{print $4}')
    
    if [[ "$status" == "Up" ]] || [[ "$status" == "running" ]]; then
        echo -e "   ${GREEN}${CHECK}${NC} ${container}: ${GREEN}Running${NC}"
    else
        echo -e "   ${RED}${CROSS}${NC} ${container}: ${RED}${status}${NC}"
    fi
done <<< "$containers"

echo ""

# ================================
# Health Checks
# ================================
echo -e "${BLUE}[INFO]${NC} Running health checks..."
echo ""

all_healthy=true

for service_info in "${SERVICES[@]}"; do
    IFS='|' read -r service_name endpoint description <<< "$service_info"
    
    echo -ne "Testing ${CYAN}${description}${NC}... "
    
    # Special handling for MySQL
    if [ "$service_name" == "mysql" ]; then
        if command -v docker &> /dev/null; then
            # Try to execute mysql ping inside container
            if docker exec msa-mysql-dev mysqladmin ping -h localhost -u root -p"${MYSQL_ROOT_PASSWORD:-defaultpassword123}" &>/dev/null 2>&1 || \
               docker exec msa-mysql-prod mysqladmin ping -h localhost -u root -p"${MYSQL_ROOT_PASSWORD:-defaultpassword123}" &>/dev/null 2>&1; then
                echo -e "${GREEN}${CHECK} Healthy${NC}"
                continue
            fi
        fi
        
        # Fallback to TCP check
        if timeout 2 bash -c "cat < /dev/null > /dev/tcp/localhost/3306" 2>/dev/null; then
            echo -e "${GREEN}${CHECK} Healthy (TCP)${NC}"
        else
            echo -e "${RED}${CROSS} Unhealthy${NC}"
            all_healthy=false
        fi
        continue
    fi
    
    # HTTP health check
    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$endpoint" 2>/dev/null)
    
    if [ "$response" == "200" ]; then
        echo -e "${GREEN}${CHECK} Healthy (HTTP $response)${NC}"
    elif [ "$response" == "000" ]; then
        echo -e "${RED}${CROSS} Unreachable${NC}"
        all_healthy=false
    else
        echo -e "${YELLOW}${WARNING} Degraded (HTTP $response)${NC}"
        all_healthy=false
    fi
done

echo ""

# ================================
# Resource Usage
# ================================
echo -e "${BLUE}[INFO]${NC} Resource usage:"
echo ""

if command -v docker &> /dev/null; then
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep -E "CONTAINER|msa-" | head -10
fi

echo ""

# ================================
# Summary
# ================================
if [ "$all_healthy" = true ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}║         ${CHECK}  ALL SERVICES ARE HEALTHY  ${CHECK}                    ║${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "🌐 Access your services:"
    echo "   • Frontend:   http://localhost:3000"
    echo "   • Spring API: http://localhost:8080"
    echo "   • Python AI:  http://localhost:8000"
    echo ""
    exit 0
else
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║                                                            ║${NC}"
    echo -e "${YELLOW}║         ${WARNING}  SOME SERVICES ARE UNHEALTHY  ${WARNING}                ║${NC}"
    echo -e "${YELLOW}║                                                            ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "🔍 Troubleshooting steps:"
    echo "   1. Check logs: docker-compose -f ${COMPOSE_FILE} logs -f"
    echo "   2. Restart services: docker-compose -f ${COMPOSE_FILE} restart"
    echo "   3. Rebuild: docker-compose -f ${COMPOSE_FILE} up -d --build"
    echo ""
    exit 1
fi
