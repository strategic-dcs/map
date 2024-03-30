# Strategic DCS Web View

## Tech Stack

- Backend: A python API on FastAPI
- Frontend: ReactJS

## Development

Requirements:
- Docker

In development the app runs on a docker-compose that will create a few containers:

 - Backend (Python)
 - Frontend (ReactJS/Node)
 - Database (PostgreSQL)

To setup your dev environment, open your terminal on the root of this project.

Copy the `.env.example` to `.env` and fill it with the required fields. Then run:

```
docker network create nginx-proxy
docker run -d -p 80:80 --name nginx-proxy --network=nginx-proxy -v /var/run/docker.sock:/tmp/docker.sock:ro jwilder/nginx-proxy

docker-compose up -d --build
```

## Deployment

1. Create a .env file with the same values found on .env.example.
1. `docker network create nginx-proxy`
1. `docker run -d -p 80:80 --name nginx-proxy --network=nginx-proxy -v /var/run/docker.sock:/tmp/docker.sock:ro jwilder/nginx-proxy`
1. `docker-compose -f docker-compose.production.yml up -d --build`

## TODO

- ?
