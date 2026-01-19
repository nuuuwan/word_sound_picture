python3 workflows/generate.py "$1"

git add data/static
git add README.md
git commit -m "Ran workflows/generate.py"

git push origin main