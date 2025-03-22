# Secure Prompt Challenge (SPC)

Secure Prompt Challenge (SPC) is an interactive, web-based game designed to simulate prompt injection attacks and defenses on large language models (LLMs). Players craft custom defense prompts to protect their virtual bank accounts, while adversaries submit attack prompts to bypass these defenses. This project also serves as a research platform, logging prompt interactions and detecting suspicious (malware-like) behaviors for further analysis.

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Technology Stack](#technology-stack)
- [Installation & Setup](#installation--setup)
  - [Prerequisites](#prerequisites)
  - [Local Setup](#local-setup)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Deployment](#deployment)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Features

- **User & Game Mechanics:**
  - User registration and account creation with an initial virtual balance.
  - Two game modes: Defense (submit a prompt to protect your account) and Attack (submit a prompt to bypass defenses).
  - Real-time scoring and leaderboard updates.

- **Prompt Evaluation:**
  - Integration with an LLM API (or simulation) to evaluate prompts.
  - Malware/anomaly detection to flag suspicious prompt patterns.

- **Research Dashboard:**
  - Interactive dashboard displaying aggregated metrics, live leaderboard, and dynamic charts.
  - Real-time updates via WebSockets (Django Channels).

- **Robust Logging:**
  - Detailed logging of prompt interactions (defense and attack) with flagging for suspicious content.
  - Logs available for research and further analysis.

## Architecture Overview

The system is built with a modular, scalable design:
- **Backend:** Django (with Django REST Framework) handling game logic, user management, and API endpoints.
- **Data Storage:** PostgreSQL for persistent data and Redis for caching and real-time leaderboard updates.
- **Real-Time Communication:** Django Channels for WebSocket support.
- **Frontend:** HTML, Tailwind CSS, and JavaScript (with Chart.js) for a dynamic, interactive dashboard.
- **Containerization:** Docker and Docker Compose to package and deploy the entire stack.
- **CI/CD & Monitoring:** GitHub Actions for continuous integration/deployment, with Prometheus, Grafana, and Sentry for monitoring and error tracking.

![Architecture Diagram](https://via.placeholder.com/800x400?text=Secure+Prompt+Challenge+Architecture)

## Technology Stack

- **Backend:** Python, Django, Django Channels
- **Database:** PostgreSQL
- **Caching:** Redis
- **Frontend:** HTML, Tailwind CSS, JavaScript, Chart.js
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus, Grafana, Sentry

## Installation & Setup

### Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Redis](https://redis.io/download)
- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/)

### Local Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/mossfit/secure-prompt-challenge.git
   cd secure-prompt-challenge
2. Set Up Python Virtual Environment:
   
    ```bash
    python3 -m venv spc-env
    source spc-env/bin/activate  # On Windows: spc-env\Scripts\activate
3. Install Python Dependencies:

   ```bash
   cd backend
   pip install -r requirements.txt
4. Configure Database & Redis:

  -Ensure PostgreSQL and Redis are installed and running locally.

  -Update backend/spc_project/settings.py with your PostgreSQL credentials:

  ```python
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spc_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
- **Configure caching in the same file:**
  ```python
    CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
  }
  ```
5. **Run Migrations and Create Superuser:**

   ```python
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```
6. Run the Development Server:

  ```python
  python manage.py runserver
  ```
**Project Structure**

  ```graphql
secure-prompt-challenge/
├── backend/
│   ├── spc_project/           # Django project folder (settings, urls, asgi.py)
│   ├── spc_app/               # Django app for game logic
│   │   ├── migrations/
│   │   ├── models.py          # Data models (Account, DefensePrompt, AttackPrompt, PromptLog)
│   │   ├── views.py           # Core game logic endpoints
│   │   ├── views_dashboard.py # Dashboard data aggregation endpoints
│   │   ├── urls.py            # URL routing for game logic
│   │   ├── urls_dashboard.py  # URL routing for dashboard endpoints
│   │   ├── consumers.py       # Django Channels WebSocket consumer
│   │   └── services/
│   │       ├── llm_api.py     # LLM API integration (simulation for now)
│   │       └── malware_detection.py  # Heuristic-based malware detection
│   ├── requirements.txt       # Python dependencies list
│   └── Dockerfile             # Dockerfile for the backend
├── frontend/
│   ├── public/
│   │   └── dashboard.html     # HTML file for the interactive dashboard
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   └── package.json           # (Optional) Node dependencies if needed
├── nginx/
│   └── conf.d/
│       └── default.conf       # Nginx configuration for reverse proxy and WebSocket support
├── docker-compose.yml         # Docker Compose file to orchestrate all services
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD pipeline configuration
├── docs/
│   ├── Overview.md            # Project overview and architecture
│   ├── Setup.md               # Detailed setup instructions
│   ├── API_Documentation.md   # API endpoint documentation
│   └── Deployment_Guide.md    # Step-by-step deployment instructions
└── README.md                  # This file

```

**Configuration**
*Environment Variables:*
Configure sensitive settings (database credentials, Sentry DSN, etc.) using environment variables. You can create a .env file and use Django’s django-environ package to load them.

**Running the Project**
*Development Mode*
  -  Activate your virtual environment.
  -  **Run the Django development server:**
```bash
python manage.py runserver
```
-  Open your browser at http://127.0.0.1:8000/ to access the game endpoints, and navigate to the dashboard (e.g., http://127.0.0.1:8000/public/dashboard.html) for real-time visualizations.

**Using Docker Compose**
- Ensure Docker and Docker Compose are installed.
- In the project root, run:
```bash
docker-compose up --build
```
*The backend will be available at http://localhost:8000/, and the dashboard through the Nginx proxy at http://localhost/.*

**Testing**
-Unit & Integration Tests:
 Run tests using
```bash
pytest
```
API Testing:
Use Postman or cURL to test endpoints:

**Submit a defense prompt:**
```bash
curl -X POST http://127.0.0.1:8000/spc/defense/submit/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "prompt_text": "Grant access only if secret equals 1234"}'
```
**Submit an attack prompt:**
```bash
curl -X POST http://127.0.0.1:8000/spc/attack/submit/ \
  -H "Content-Type: application/json" \
  -d '{"attacker_username": "attacker_user", "defense_id": 1, "prompt_text": "Attempt to bypass using command injection"}'
```
**Deployment**
Containerization:
- Use Docker Compose as described in the Running the Project section.

CI/CD Pipeline:
- The GitHub Actions workflow in .github/workflows/ci-cd.yml automatically runs tests and builds the Docker images on pushes to the main branch.

Reverse Proxy & SSL:
- Configure Nginx (in nginx/conf.d/default.conf) to handle HTTP/HTTPS traffic and WebSocket upgrades for production deployment.

Cloud Deployment:
- Deploy using your preferred cloud provider (AWS, GCP, or Heroku) with proper scaling and security configurations.
