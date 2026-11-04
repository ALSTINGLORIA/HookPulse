# HookPulse

A backend service that accepts events through a REST API and delivers them asynchronously to external webhook endpoints.

Built using **FastAPI, Redis, Celery, HTTPX, and Docker Compose**, this project demonstrates how background task processing can improve the responsiveness and separation of backend services.

## 1. Project Overview

In modern applications, events such as order creation, payment completion, and user registration often need to be communicated to external services.

Sending webhook requests directly inside an API endpoint can cause delays, especially when external services respond slowly or become unavailable.

HookPulse solves this problem by separating event acceptance from webhook delivery.

The API receives and stores events, queues background tasks, and allows independent workers to handle webhook delivery.

### Core Functionality

- Accept events through a REST API.
- Validate incoming event data using Pydantic.
- Generate unique IDs for events.
- Store event information in Redis.
- Queue background delivery tasks using Celery.
- Deliver events to external webhook URLs using HTTPX.
- Update event status based on delivery results.
- Run the API, Redis, and Celery worker using Docker Compose.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Primary programming language |
| FastAPI | REST API development |
| Pydantic v2 | Request and response validation |
| Redis | Event storage, message broker, and result backend |
| Celery | Background task processing |
| HTTPX | HTTP webhook delivery |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |

## 3. System Architecture

HookPulse follows a producer-consumer architecture.

- **FastAPI:** Receives incoming events and submits background tasks.
- **Redis:** Stores event information and acts as the Celery message broker.
- **Celery Worker:** Consumes queued tasks and processes webhook deliveries.
- **HTTPX:** Sends HTTP POST requests to external webhook endpoints.

### Event Processing Workflow

1. A client submits an event through the FastAPI endpoint.
2. FastAPI validates the request using the Pydantic schema.
3. The application generates a unique event ID.
4. Event information is stored in Redis.
5. FastAPI publishes a Celery task containing the event ID.
6. The Celery worker receives the task from Redis.
7. The worker retrieves the corresponding event from Redis.
8. HTTPX sends the event payload to the target webhook URL.
9. The event status is updated based on the delivery result.
10. Celery stores the task execution result in its result backend.

## 4. Redis Architecture

HookPulse uses three logical Redis databases to separate application data from Celery's internal operations.

| Redis Database | Responsibility |
|---|---|
| DB 0 | Stores application event information |
| DB 1 | Acts as the Celery message broker |
| DB 2 | Acts as the Celery result backend |

### DB 0 — Event Storage

Stores event details such as the event ID, event type, target URL, payload, delivery status, and attempt count.

### DB 1 — Message Broker

Stores task messages published by FastAPI for Celery workers to consume. These messages contain task information and the corresponding event ID.

### DB 2 — Result Backend

Stores execution results and task state information managed by Celery.

All three databases operate on the same Redis server but serve separate logical purposes.

## 5. Project Structure

```text
HookPulse/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── events.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── redis.py
│   │   └── celery_app.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── event.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── event_service.py
│   │
│   └── tasks/
│       ├── __init__.py
│       └── delivery.py
│
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .dockerignore
└── .gitignore
```

### Directory Responsibilities

| Directory | Responsibility |
|---|---|
| `api/` | Handles incoming API requests |
| `core/` | Contains Redis and Celery configuration |
| `schemas/` | Defines request and response schemas |
| `services/` | Contains event creation logic |
| `tasks/` | Contains Celery background tasks |
| `tests/` | Reserved for automated tests |

## 6. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns basic application information |
| GET | `/health` | Checks API application health |
| POST | `/events/` | Accepts an event and queues it for delivery |

### Event Submission

The `POST /events/` endpoint accepts:

- `event_type` — Type of event being submitted.
- `target_url` — External webhook destination.
- `payload` — Data to be delivered.

After successful submission and task queuing, the API returns:

- A unique event ID.
- The current event status.
- A confirmation message.

The endpoint returns HTTP `202 Accepted`, indicating that the event has been accepted for asynchronous processing.

## 7. Background Task Processing

Celery is used to execute webhook delivery independently of the FastAPI request lifecycle.

The API publishes tasks using Celery's `.delay()` method.

The worker receives the task, retrieves the event information from Redis, and performs the HTTP request.

This separation allows the API to respond without waiting for external webhook delivery to finish.

## 8. Docker Environment

HookPulse uses Docker Compose to run three independent services.

| Service | Description |
|---|---|
| `api` | Runs the FastAPI application |
| `redis` | Provides Redis storage and messaging |
| `worker` | Executes Celery background tasks |

The services communicate through Docker's internal network using their Compose service names.

Redis data is persisted using a Docker volume, with Redis append-only file persistence enabled.

## 9. Running the Project

### Prerequisites

- Docker
- Docker Compose
- Git

### Setup

Clone the repository:

```bash
git clone <your-repository-url>
cd HookPulse
```

Configure the `.env` file with the Redis connection settings.

Build and start the services:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker compose ps
```

### Access the Application

| Resource | URL |
|---|---|
| API | http://localhost:8000 |
| Swagger Documentation | http://localhost:8000/docs |
| API Health Check | http://localhost:8000/health |

### Useful Docker Commands

```bash
# View running containers
docker compose ps

# View worker logs
docker compose logs -f worker

# View API logs
docker compose logs -f api

# Access Redis CLI
docker compose exec redis redis-cli

# Stop services
docker compose down
```

## 10. Project Summary

HookPulse demonstrates an asynchronous backend architecture for handling and delivering webhook events.

By combining FastAPI, Redis, and Celery, the system separates API request handling from background processing.

The application provides event submission, Redis-based event storage, task queuing, background webhook delivery, and basic delivery status tracking.