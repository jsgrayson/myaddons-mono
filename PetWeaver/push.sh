#!/bin/bash
# Quick push script for PetWeaver

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== PetWeaver Git Push Script ===${NC}\n"

# Check if we have a remote configured
if ! git remote | grep -q origin; then
    echo -e "${RED}No remote 'origin' configured!${NC}"
    echo "To add a remote, run:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/petweaver.git"
    exit 1
fi

# Get current branch
BRANCH=$(git branch --show-current)

echo -e "${BLUE}Current branch:${NC} $BRANCH"
echo ""

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo -e "${BLUE}Uncommitted changes detected. Adding all changes...${NC}"
    git add -A
    
    # Prompt for commit message
    echo ""
    echo -e "${GREEN}Enter commit message:${NC}"
    read -r COMMIT_MSG
    
    if [[ -z "$COMMIT_MSG" ]]; then
        echo -e "${RED}Commit message cannot be empty!${NC}"
        exit 1
    fi
    
    git commit -m "$COMMIT_MSG"
else
    echo -e "${GREEN}✓ No uncommitted changes${NC}"
fi

# Push to remote
echo ""
echo -e "${BLUE}Pushing to origin/$BRANCH...${NC}"
git push -u origin "$BRANCH"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Successfully pushed to GitHub!${NC}"
else
    echo ""
    echo -e "${RED}✗ Push failed. Check your GitHub credentials and remote URL.${NC}"
    exit 1
fi
