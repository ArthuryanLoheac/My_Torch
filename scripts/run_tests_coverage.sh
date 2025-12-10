#!/usr/bin/env bash
##
## EPITECH PROJECT, 2025
## My_Torch
## File description:
## Script pour lancer tous les tests avec couverture de code
##

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Tests Unitaires - My_Torch (Coverage)${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 n'est pas installé${NC}"
    exit 84
fi

cd "$(dirname "$0")/.." || exit 84

if ! python3 -m pytest --version &> /dev/null; then
    echo -e "${YELLOW}⚠️  pytest n'est pas installé. Installation...${NC}"
    python3 -m pip install pytest pytest-cov --quiet
fi

if ! python3 -c "import pytest_cov" &> /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  pytest-cov n'est pas installé. Installation...${NC}"
    python3 -m pip install pytest-cov --quiet
fi

echo -e "${BLUE}Lancement des tests avec couverture...${NC}"
echo ""

python3 -m pytest tests/ \
    --cov=fen_parser \
    --cov-report=term-missing \
    --cov-report=html \
    -v

exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}✅ Tous les tests sont passés !${NC}"
    echo ""
    echo -e "${BLUE}📊 Rapport HTML généré dans : htmlcov/index.html${NC}"
    echo -e "${BLUE}   Ouvrez-le avec : xdg-open htmlcov/index.html${NC}"
else
    echo -e "${RED}❌ Certains tests ont échoué${NC}"
fi

echo ""
exit $exit_code
