
---

# Assignment Submission Portal Setup Guide

This guide provides instructions to set up and run the Assignment Submission Portal using Docker. Docker will install all requirements from the `requirements.txt` file and set up a MongoDB service. Follow these steps carefully.

## Prerequisites

- Ensure Docker and Docker Compose are installed on your system.

---

## Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone Sajad-Lx/growthx_assignment
cd growthx_assignment
```

---

## Step 2: Create a `.env` file

Create a new file with name `.env` in the project directory and type the following content:

```bash
MONGO_DB=database_name
MONGO_USERNAME=root
MONGO_PASSWORD=database_password
SECRET_KEY=your_special_secret_key
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Step 3: Build the Docker Image

Use Docker Compose to build the application and MongoDB services. Run the following command in the root of the project directory:

```bash
docker-compose up --build
```

- This command will:
  - Build the application image using the `Dockerfile`.
  - Set up MongoDB as a service, as defined in the `docker-compose.yml` file.

---

## Step 4: Access the Application

Once Docker has finished building and running the containers, you can access the FastAPI application on:

```
http://localhost:8000
```

### Access the Swagger UI

To test the API endpoints, navigate to:

```
http://localhost:8000/docs
```

Swagger UI provides an interactive interface for testing the APIs.

---

## Step 5: Using OAuth2 for Secured APIs

1. **Authorize Button**:
   - Click the **Authorize** button in the Swagger UI and enter the `username` and `password` for authorization.
   - You can also use `cURL` and pass the Bearer token you obtain from the `/login` or `/token` endpoint.
   
2. **Test APIs**:
   - After authorizing, you can test all secured endpoints (e.g., assignment upload, assignment status update, etc.).
   - Ensure to provide the OAuth2 Bearer token in the format: `Bearer <your_token>`.

---

## Step 6: Stopping the Containers

To stop the application and MongoDB services, run:

```bash
docker-compose down
```

This will stop and remove the containers.

---

### Notes

- Make sure to modify the environment variables (e.g., MongoDB credentials, secret keys) in the `.env` file according to your setup.
- The application logs can be viewed using:

```bash
docker-compose logs
```

- If you need to rebuild the Docker image (after changes to the code or requirements), use:

```bash
docker-compose up --build
```

---

That's it! You've successfully set up the Assignment Submission Portal using Docker. You can now test and interact with the APIs via Swagger UI.

---