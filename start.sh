#!/bin/sh

ENV=${1}
echo "env: $ENV"

/bin/nohup ./scripts/gn_di.sh &
java -Dspring.profiles.active=$ENV -Dfile.encoding=UTF-8 -jar ndata-0.0.1-SNAPSHOT.jar 
