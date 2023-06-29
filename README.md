# Strategic DCS Web View

## Tech Stack

- Backend: A python API on FastAPI
- Frontend: ReactJS

## Development

In development the app runs on a docker-composer that will create a few containers:

 - Backend (Python)
 - Frontend (ReactJS/Node)
 - Database (MySQL)

To start development, on the root of the repository run:

`docker-compose build .`

`TODO`: Need to direct on how to get the DISCORD-ID.

Run this once you have your DISCORD_ID:

`docker-compose run -e TEST_DISCORD_USER_ID=<DISCORD-ID> --rm backend python scripts/db_setup.py`

This will setup the DB with Syria an a single user on `blue` side.

You can now visit: http://localhost:3000/ to see the application.

## Deployment

`TODO`
