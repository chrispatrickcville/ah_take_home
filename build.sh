# Syntax: ./build.sh
# Use --no-cache=true  when necessary
VERSION_TAG=$(<VERSION)
docker build -t chrispatrick/ah-take-home:$VERSION_TAG .