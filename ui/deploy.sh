npm run build
host=wa
scp -r dist/static/ $host:/var/www/sariel/
scp -r dist/index.html $host:/var/www/sariel/
