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
# If you already have the proxy in place with the name nginx-proxy, skip to step 3
# 1. creates the network
docker network create nginx-proxy

# 2. start the nginx proxy
docker run -d -p 80:80 --name nginx-proxy --network=nginx-proxy -v /var/run/docker.sock:/tmp/docker.sock:ro jwilder/nginx-proxy

# 3. build the images and start the containers
docker-compose up -d --build

# 4. Creates the tables
docker-compose exec db sh -c "mysql -u root -p password < dev-data/schema.sql"

# 5. Seed the DB with sample data
docker-compose exec db sh -c "mysql -u root -p password sdcs < dev-data/seed.sql"
```

Next, you'll need your DISCORD_ID, here's how to get it:

- On Discord, go to Settings > Advanced
- Scroll down and make sure that Developer Mode is on
- Exit your settings and type a message in any channel on any server
- Right-click your profile picture and click 'Copy ID'

Then execute:

```
# Updates the seeded user with your discord ID
docker-compose exec db sh -c "mysql -u root -p password sdcs -e 'UPDATE user SET discord_id=<REPLACE-WITH-DISCORD-ID>' WHERE id=1"
```

You can now visit: http://localhost/ to see the application.

## Deployment

`TODO`
