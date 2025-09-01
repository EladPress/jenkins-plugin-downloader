set -x
set -e

JENKINS_VERSION=$1
CONTAINER=jenkins-$JENKINS_VERSION
IMAGE=jenkins/jenkins:$JENKINS_VERSION

docker run -d -v $PWD/:/tmp/jenkins-plugins/ --name $CONTAINER $IMAGE

docker cp ./plugins.txt $CONTAINER:/tmp/jenkins-plugins/plugins.txt
docker exec $CONTAINER jenkins-plugin-cli --plugin-file /tmp/jenkins-plugins/plugins.txt --jenkins-version $JENKINS_VERSION --plugin-download-directory /tmp/jenkins-plugins/plugins/ #--plugins delivery-pipeline-plugin:1.3.2 deployit-plugin

docker rm -f $CONTAINER
docker rmi -f $IMAGE