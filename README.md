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

# 3. Copy the .env.example and rename it to .env 
cp .env.example .env

# now replace its contents.

# 4. build the images and start the containers
docker-compose up -d --build

# 5. Creates the tables (password is `password`)
docker-compose exec db sh -c "mysql -u root < dev-data/schema.sql"

# 6. Seed the DB with sample data
docker-compose exec db sh -c "mysql -u root sdcs < dev-data/seed.sql"
```

Next, you'll need your DISCORD_ID, here's how to get it:

- On Discord, go to Settings > Advanced
- Scroll down and make sure that Developer Mode is on
- Exit your settings and type a message in any channel on any server
- Right-click your profile picture and click 'Copy ID'

Then execute:

```
# Updates the seeded user with your discord ID
# WARNING: this will set all users with the same discord_id. Include your ID to the query if you know your users ID.
docker-compose exec db sh -c "mysql -u root sdcs -e 'UPDATE user SET discord_id=<REPLACE-WITH-DISCORD-ID>'"
```

You can now visit: http://localhost/ to see the application.

## Deployment

`TODO`
