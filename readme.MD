# OEI (Orbital Edge Imaging) Project

This project was developed as part of a technical challenge. It simulates a fictional company, Orbital Edge Imaging (OEI), providing a web-based application to request satellite tasking and visualize orbital passes. The system includes a RESTful API built with FastAPI, a PostgreSQL database with PostGIS support, and a frontend developed in TypeScript using React and Vite.

This project is a proof of concept and is not intended for use in a production environment. It does not implement user management, authentication, authorization, API keys, or rate limiting. Test coverage is minimal or absent, and some bugs may be present. The primary goal is to demonstrate system architecture, integration of components, and the ability to deliver a functional full-stack application.

## Overview

This is a full-stack application composed of:

- **Frontend**: React with Vite, written in TypeScript.
- **Backend**: FastAPI (Python), using SQLAlchemy 2.0 for ORM and Alembic for database migrations.
- **Database**: PostgreSQL with the PostGIS extension for geospatial data support.

## Prerequisites

Software required in your system:
- Docker
- Docker Compose

## Setup & Run

Clone the repository:
```bash
 git clone https://github.com/oplaco/oei.git
```

Navigate to the project root and start the services:

```bash
docker-compose up --build
```

This builds and starts three services (please make sure all the ports are free otherwise it might not work):
1. PostgreSQL: with PostGIS, available on port 5432
2. api: FastAPI backend, accessible at http://localhost:8000
3. frontend: React + Vite frontend, accessible at http://localhost:5173

## Migrations (Backend)
After the containers are running, apply the database migrations inside the `api` container:

```bash
docker-compose exec api alembic upgrade head
```

## Environment configuration
- Create root-level .env file (used by Docker compose)

```
POSTGRES_DB=oei
POSTGRES_USER=oei
POSTGRES_PASSWORD=oei
DATABASE_URL=postgresql+psycopg2://oei:oei@db:5432/oei
```

- Create frontend-level .env file apps/frontend/.env

```
VITE_API_BASE_URL=http://localhost:8000
```

## Stopping services
```bash
docker-compose down
```

## Frontend usage

Once all the services are up an running access the frontend. The frontend consists of two main pages::
- Landing Page. 
    - A minimal introductory page representing the company website.
    - In a real-world scenario, this page would present your brand, products, or vision.
    - You can navigate to the main application by clicking the "Try Demo" button.
- Map Page. This is the core of the application. It is divided into two main sections:
    - Left column. Contains:
        - Area of Interest (AOI) upload. Upload a polygon (in GeoJSON format) with a custom name.
        - Satellite selection. Use the dropdown to select a satellite from those already available in the system. The selected satellite will be used for pass prediction.
        - TLE input. Paste one or more TLE (Two-Line Element) messages to register new satellites. These are immediately available for selection.
        - Pass computation. Once an AOI and a satellite are selected, you can compute orbital passes (visibility windows).
    - Righ column. Map Viewer.
        - An interactive map built with Leaflet.
        - Automatically zooms to relevant geometry upon uploads or pass computation.