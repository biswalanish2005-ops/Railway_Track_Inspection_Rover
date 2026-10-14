#!/bin/bash
# Autonomous Railway Track Inspection Rover — GitHub Push & Deployment Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================================"
echo "  🚆 PUSHING TO GITHUB & DEPLOYING GITHUB PAGES"
echo "  Repository: https://github.com/biswalanish2005-ops/Railway_Track_Inspection_Rover.git"
echo "========================================================================"

# Ensure both branches are aligned
git branch -f gh-pages main

echo "[*] Pushing 'main' branch (source code, ROS 2 packages & GitHub Actions workflow)..."
git push -u origin main

echo "[*] Pushing 'gh-pages' branch (static web inspection portal & track assets)..."
git push -u origin gh-pages

echo ""
echo "========================================================================"
echo "✅ CODE PUSH COMPLETE!"
echo ""
echo "🌐 GitHub Repository:   https://github.com/biswalanish2005-ops/Railway_Track_Inspection_Rover"
echo "🌐 Live GitHub Pages:   https://biswalanish2005-ops.github.io/Railway_Track_Inspection_Rover/"
echo "========================================================================"
