# Mock-API-XIVA-MOB
Mock API's for xiva mobile dev

git pull https://github.com/arsalanissm/Mock-API-XIVA-MOB.git

cd in directory to docker file
docker build -t mock_api .
docker run -d -p 8000:8000 mock_api
docker ps -a --> verify container
docker logs -f [CONTAINER ID] --> to view logs

