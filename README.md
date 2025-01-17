﻿Flask MongoDB CRUD API
Welcome to the Flask MongoDB CRUD API project! This guide will walk you through setting up and running the application, which uses Flask for the API and MongoDB for data storage. We'll be using Docker to simplify the setup process. Let's get started!

Prerequisites
Before we begin, make sure you have the following installed on your machine:

Docker: If you don't have it, you can download it here.
Postman: This is a handy tool for testing API endpoints. Download it here.
Step 1: Clone the Repository
First, you'll need to get a copy of the project on your local machine. Open your terminal or command prompt and run:

sh
Copy code
git clone https://github.com/your-username/your-repo.git
cd your-repo
Step 2: Create the requirements.txt File
In the root directory of the project, create a file named requirements.txt and add the following lines to it. This file lists the Python packages our application needs:

plaintext
Copy code
Flask==2.0.2
flask_pymongo==2.3.0
pymongo==4.0.2
werkzeug==2.0.2
Step 3: Set Up Docker
We’ll use Docker to containerize our application and MongoDB. This makes it easier to manage dependencies and ensures consistency across different environments.

Create a Dockerfile
Create a file named Dockerfile in the root directory and add the following content:

Dockerfile
Copy code
# Use the latest official Python image as a base
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run the application
CMD ["python", "app.py"]
Create a docker-compose.yml File
Next, create a docker-compose.yml file in the root directory with the following content. This file defines the services (Flask and MongoDB) and their configurations:

yaml
Copy code
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

  flaskapp:
    build: .
    container_name: flaskapp
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
    environment:
      - MONGO_URI=mongodb://mongodb:27017/yourdbname

volumes:
  mongo-data:
Step 4: Build and Run the Application
Now, we’re ready to build and run our Docker containers.

Open your terminal or command prompt.

Navigate to your project directory.

Run the following command to build and start the containers:

sh
Copy code
docker-compose up --build
This command tells Docker to build the images and start the containers based on the configurations in your Dockerfile and docker-compose.yml.

Your Flask application should now be running on http://localhost:8000.

Step 5: Test the API Endpoints with Postman
You can use Postman to test the API endpoints. Here are the endpoints available:

Create a User
URL: http://localhost:8000/user

Method: POST

Request Body:

json
Copy code
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "password123"
}
Get All Users
URL: http://localhost:8000/userlist
Method: GET
Get a User by ID
URL: http://localhost:8000/user/<id>
Method: GET
URL Params: id=[string]
Update a User by ID
URL: http://localhost:8000/user/<id>

Method: PUT

URL Params: id=[string]

Request Body:

json
Copy code
{
  "name": "John Doe Updated",
  "email": "john.updated@example.com",
  "password": "newpassword123"
}
Delete a User by ID
URL: http://localhost:8000/user/<id>
Method: DELETE
URL Params: id=[string]
Troubleshooting
If you run into issues, here are a few tips:

Ensure Docker and Docker Compose are installed and running correctly.

Check that no other services are using ports 8000 or 27017.

If you see a 500 Internal Server Error, check the logs for more details:

sh
Copy code
docker logs flaskapp
If MongoDB connection issues occur, make sure the MongoDB service is running and accessible.
With this the application should be able to run succesfully.
