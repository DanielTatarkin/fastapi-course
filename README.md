### FastAPI Blog example




#### PostgreSQL setup
- **database.env**: Stores environment variables for PostgreSQL to read from when initializing (DB username, password etc.)
- **docker-compose.yml**: Docker Compose file to set up local PostgreSQL instance
    - To run: "docker-compose up" or "docker-compose up -d"
    - To stop: "docker-compose down"
    - To delete volumes "docker-compose down --volumes"