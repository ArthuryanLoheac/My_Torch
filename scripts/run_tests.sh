#!/usr/bin/env bash
##
## EPITECH PROJECT, 2025
## My_Torch
## File description:
## Script pour lancer les tests unitaires du parser FEN
##

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  Tests Unitaires - FEN Parser${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 n'est pas installé${NC}"
    exit 84
fi

cd "$(dirname "$0")/.." || exit 84

echo -e "${BLUE}Lancement des tests...${NC}"
echo ""

python3 tests/test_fen_parser.py

exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}✅ Tous les tests sont passés !${NC}"
else
    echo -e "${RED}❌ Certains tests ont échoué${NC}"
fi

exit $exit_code
