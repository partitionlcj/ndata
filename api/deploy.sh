mvn clean package -DskipTests=true
scp target/ndata-0.0.1-SNAPSHOT.jar parrot:~/app/ndata
