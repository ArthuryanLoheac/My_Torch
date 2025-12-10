#!/usr/bin/env bash
##
## EPITECH PROJECT, 2025
## My_Torch - Bonus
## File description:
## Script d'installation des dépendances pour l'interface graphique
##

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  My_Torch - Installation des dépendances BONUS${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 n'est pas installé${NC}"
    echo -e "${YELLOW}Installez Python3 avant de continuer${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python3 trouvé: $(python3 --version)"
echo ""

if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo -e "${RED}❌ pip n'est pas installé${NC}"
    echo -e "${YELLOW}Installez pip avant de continuer${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} pip trouvé"
echo ""

echo -e "${BLUE}Installation des dépendances...${NC}"
echo ""

dependencies=("python-chess" "pygame" "numpy")

for dep in "${dependencies[@]}"; do
    echo -e "${YELLOW}Installation de ${dep}...${NC}"
    python3 -m pip install --user "$dep" --quiet

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} ${dep} installé"
    else
        echo -e "${RED}✗${NC} Erreur lors de l'installation de ${dep}"
    fi
done

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}✅ Installation terminée !${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${BLUE}Pour lancer l'interface graphique :${NC}"
echo -e "  ${YELLOW}cd bonus${NC}"
echo -e "  ${YELLOW}python3 chess_board_viewer.py${NC}"
echo ""
