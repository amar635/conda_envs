#### Resource: https://aws.amazon.com/tutorials/serve-a-flask-app/
#### Resource: https://aws.amazon.com/getting-started/guides/setup-environment/
#### Resource: https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-install-software#install-software-lightsailctl


### Create a FLASK APP
mkdir lightsail-containers-flask
cd lightsail-containers-flask

### Create an app.py file
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   return "Hello, World!"

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)

### Create requirements.txt
flask===3.0.0

### Create a Dockerfile
#### Set base image (host OS)
FROM python:3.12-alpine

#### By default, listen on port 5000
EXPOSE 5000/tcp

#### Set the working directory in the container
WORKDIR /app

#### Copy the dependencies file to the working directory
COPY requirements.txt .

#### Install any dependencies
RUN pip install -r requirements.txt

#### Copy the content of the local src directory to the working directory
COPY app.py .

#### Specify the command to run on container start
CMD [ "python", "./app.py" ]


### Directory Structure
$ tree
.

├── app.py
├── Dockerfile
└── requirements.txt

0 directories, 3 files
$

### Build a Docker Image
docker build -t flask-container .

### Run the Docker Container
docker run -p 5000:5000 flask-container

### Create a container Service
aws lightsail create-container-service --service-name flask-service --power small --scale 1
                                        OR
aws lightsail create-container-service --service-name flask-service --power nano --scale 1

### Check the container services
aws lightsail get-container-services

### Push the docker image to lightsail container
aws lightsail push-container-image --service-name flask-service --label flask-container --image flask-container

### Create a containers.json file
{
    "flask": {
        "image": ":flask-service.flask-container.X",
        "ports": {
            "8080": "HTTP"
        }
    }
}

### Create a public-endpoint.json file
{
    "containerName": "flask",
    "containerPort": 8080
}
### Create a container deployment service
aws lightsail create-container-service-deployment --service-name flask-service --containers file://containers.json --public-endpoint file://public-endpoint.json


### Clean up
aws lightsail delete-container-service --service-name flask-service

### Check the container services
aws lightsail get-container-services
