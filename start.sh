#!/bin/sh

ENV=${1}
echo "env: $ENV"

pushd scripts
/bin/nohup ./gn_di.sh &
popd
java -Dspring.profiles.active=$ENV -Dfile.encoding=UTF-8 -jar ndata-0.0.1-SNAPSHOT.jar 
