@echo off
git init
git remote remove origin
git remote add origin https://github.com/rhlfur2055-prog/codemaster-next
git branch -M main
git add .
git commit -m "Push to new repo"
git push -u origin main
