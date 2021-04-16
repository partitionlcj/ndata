npm run build
host=parrot
scp -r dist/* $host:/var/www/html/ndata/
