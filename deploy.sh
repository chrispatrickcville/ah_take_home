# Syntax: ./deploy.sh
VERSION_TAG=$(<VERSION)
docker push chrispatrick/ah-take-home:$VERSION_TAG