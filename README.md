# Strategic DCS Web View

## Tech Stack

- Backend: A python API on FastAPI
- Frontend: ReactJS

## Development

Requirements:
- Docker

In development the app runs on a docker-composer that will create a few containers:

 - Backend (Python)
 - Frontend (ReactJS/Node)
 - Database (MySQL)

To setup your dev environment, open your terminal on the root of this project.


Copy the `.env.example` to `.env` and fill it with the required fields. Then run:

```
docker network create nginx-proxy
docker run -d -p 80:80 --name nginx-proxy --network=nginx-proxy -v /var/run/docker.sock:/tmp/docker.sock:ro jwilder/nginx-proxy

docker-compose up -d --build
```

You need MySQL running along with the SDCS Engine.

If you don't already have MySQL running, you can do:

`docker run -d -p 3306:3306 --name sdcs-mysql -e MYSQL_ALLOW_EMPTY_PASSWORD=1 -v sdcs-mysql-data:/var/lib/mysql mysql:8.0.33`

You can now visit: http://localhost/ to see the application.

## Deployment

`TODO`

1. Backend: Create a .env file with the same values found on .env.example.

## TODO

- Add Strategic DCS logo
- Add FARPs
- Add Info panel that shows info on the Airfield/FARP.
