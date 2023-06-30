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

To setup your dev environment, open your terminal on the root of this project, then run:

```
docker network create nginx-proxy
docker run -d -p 80:80 --name nginx-proxy --network=nginx-proxy -v /var/run/docker.sock:/tmp/docker.sock:ro jwilder/nginx-proxy

docker-compose up -d --build

docker-compose exec db sh -c "mysql -u root -p password < dev-data/schema.sql"
docker-compose exec db sh -c "mysql -u root -p password sdcs < dev-data/seed.sql"
```

Next, you'll need your DISCORD_ID, here's how to get it:

- On Discord, go to Settings > Advanced
- Scroll down and make sure that Developer Mode is on
- Exit your settings and type a message in any channel on any server
- Right-click your profile picture and click 'Copy ID'

Then execute:

`docker-compose exec db sh -c "mysql -u root -p password sdcs -e 'UPDATE user SET discord_id=<REPLACE-WITH-DISCORD-ID>'"`

You can now visit: http://localhost/ to see the application.

## Deployment

`TODO`
