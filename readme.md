QR CODE GENERATOR – DOCKERIZED APPLICATION WITH GITHUB ACTIONS

--------------------------------------------------
PROJECT OVERVIEW
--------------------------------------------------

This project is a Python-based QR Code Generator that generates QR codes from a given URL.

The application is containerized using Docker and automatically builds and pushes Docker images
to Docker Hub using GitHub Actions CI/CD.

Features:
- Accepts URL input
- Generates QR code image
- Stores QR codes in configurable directory
- Logs activity
- Uses environment variables
- Runs inside Docker container
- Automated CI/CD pipeline

--------------------------------------------------
PREREQUISITES
--------------------------------------------------

1. Python (3.10+)

Check installation:
python --version

2. Docker

docker --version

3. Git

git --version

4. GitHub account
https://github.com

5. Docker Hub account
https://hub.docker.com

--------------------------------------------------
PROJECT STRUCTURE
--------------------------------------------------

qr-code-generator
│
├── main.py
├── requirements.txt
├── Dockerfile
├── .env
├── .gitignore
│
└── .github
    └── workflows
        └── docker.yml

--------------------------------------------------
STEP 1 – CREATE PROJECT
--------------------------------------------------

mkdir qr-code-generator
cd qr-code-generator

--------------------------------------------------
STEP 2 – INSTALL DEPENDENCIES
--------------------------------------------------

pip install -r requirements.txt

requirements.txt

qrcode[pil]
Pillow
python-dotenv

--------------------------------------------------
STEP 3 – ENVIRONMENT VARIABLES
--------------------------------------------------

Create .env file

LOG_PATH=logs
QR_PATH=qr_codes
DEFAULT_URL=https://www.njit.edu

--------------------------------------------------
STEP 4 – RUN APPLICATION LOCALLY
--------------------------------------------------

Run with URL:

python main.py --url https://www.njit.edu

Run using default URL:

python main.py

QR codes will be generated in:

qr_codes/

Logs will be written to:

logs/app.log

--------------------------------------------------
STEP 5 – INITIALIZE GIT
--------------------------------------------------

git init
git add .
git commit -m "Initial commit"

Create GitHub repository then connect:

git branch -M main
git remote add origin https://github.com/<username>/qr-code-generator.git
git push -u origin main

--------------------------------------------------
STEP 6 – DOCKERFILE
--------------------------------------------------

FROM python:3.12-slim-bullseye

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m myuser && mkdir logs qr_codes && chown myuser:myuser logs qr_codes

COPY --chown=myuser:myuser . .

USER myuser

ENTRYPOINT ["python", "main.py"]
CMD ["--url", "https://www.njit.edu"]

--------------------------------------------------
STEP 7 – BUILD DOCKER IMAGE
--------------------------------------------------

docker build -t qr-code-generator-app .

--------------------------------------------------
STEP 8 – RUN DOCKER CONTAINER
--------------------------------------------------

docker run --name qr-generator qr-code-generator-app

Run with custom URL:

docker run qr-code-generator-app --url https://google.com

--------------------------------------------------
STEP 9 – MOUNT VOLUME FOR QR OUTPUT
--------------------------------------------------

Create local directory

mkdir qr_codes

Run container with volume

docker run -v $(pwd)/qr_codes:/app/qr_codes qr-code-generator-app --url https://google.com

Generated QR codes will appear in the local folder.

--------------------------------------------------
STEP 10 – PUSH IMAGE TO DOCKER HUB
--------------------------------------------------

Login

docker login

Tag image

docker tag qr-code-generator-app <dockerhub-username>/qr-code-generator-app

Push image

docker push <dockerhub-username>/qr-code-generator-app

Test image

docker run <dockerhub-username>/qr-code-generator-app --url https://github.com

--------------------------------------------------
STEP 11 – GITHUB ACTIONS WORKFLOW
--------------------------------------------------

Create file

.github/workflows/docker.yml

Workflow content:

name: Build and Push Docker Image

on:
  push:
    branches: ["main"]
  workflow_dispatch:

jobs:
  docker:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v5

      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/qr-code-generator-app:latest

--------------------------------------------------
STEP 12 – ADD GITHUB SECRETS
--------------------------------------------------

Go to:

Repository → Settings → Secrets and Variables → Actions

Add two secrets:

DOCKERHUB_USERNAME
DOCKERHUB_TOKEN

Create token in DockerHub:

Docker Hub → Account Settings → Security → Access Token

--------------------------------------------------
STEP 13 – TRIGGER WORKFLOW
--------------------------------------------------

git add .
git commit -m "Trigger workflow"
git push

Check status in:

GitHub → Actions

Docker image will automatically build and push.

--------------------------------------------------
STEP 14 – VERIFY FINAL IMAGE
--------------------------------------------------

docker run <dockerhub-username>/qr-code-generator-app --url https://njit.edu

--------------------------------------------------
FINAL DELIVERABLES
--------------------------------------------------

- Python QR Code Generator
- Dockerized application
- DockerHub image
- GitHub repository
- GitHub Actions CI/CD pipeline
- Documentation