# cloud-computing framewiz

## Description
This cloud-computing project is an implementation of API creation for FrameWiz application. The API is responsible for responding to login register and face detection requests from users. This API is run on the backend and interacts with the Google cloud app engine computing service.

## System Requirements
- python39
- sql
- google cloud (app engine,sql,cloud storage)
- other library in file requirements.txt

## Instalization
- Install the libraries needed in the project and collect them in the requirements.txt file:
`pip install -r requrements.txt`

- Download the model folder and put it in this folder, for the following install folder link:
https://console.cloud.google.com/storage/browser/capstone-c23ps466-1-tf2-models 

## Configuration
- Enable sql services
- Select MySQL, then create an instance name and password as well as region and connection.
- If you have entered phpmyadmin.co to be more free in creating a database
- Create the app.yaml file
- Fill in the file according to the configuration required by the application, such as in our application requires instance class F4_1 and memory size 10 gb.

## Deploy
- Enable authentication
`gcloud auth login`

- Deploy using app engine computing
`gcloud app deploy`

## Usage
Access the API using the appropriate endpoint
base url: https://service-dot-capstone-c23-ps466.et.r.appspot.com 
1. "POST /register": to register a user account
2. "POST /login": to use the registered account
3. "POST /predict": to perform face image detection