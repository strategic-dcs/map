# Strategic DCS Web View

## Tech Stack

- Backend: A python API on FastAPI
- Frontend: ReactJS

## Development

In development the app runs on a docker-composer that will create a few containers:

 - Backend (Python)
 - Frontend (ReactJS/Node)
 - Database (MySQL)

First, to start development, on the root of the repository run:

`docker-compose up -d`

Second, you'll need your discord_id to test the app. Here's how to find it:

- On Discord, go to Settings > Advanced
- Scroll down and make sure that Developer Mode is on
- Exit your settings and type a message in any channel on any server
- Right-click your profile picture and click 'Copy ID'

Now run the following on our terminal:

`docker-compose run -e TEST_DISCORD_USER_ID=<DISCORD-ID> --rm backend python scripts/db_setup.py`

This will setup the DB with Syria an a single user (your user) on `blue` side.

You can now visit: http://localhost:3000/ to see the application.

## Deployment

`TODO`
