npm run build
host=parrot
scp -r dist/static/ $host:/var/www/html/ndata/
scp -r dist/index.html $host:/var/www/html/ndata/
