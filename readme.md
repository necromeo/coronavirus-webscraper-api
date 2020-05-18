# Coronavirus data fetching

This is a very simple API created with the fantastic FastAPI framework :snake:.

Its usage is really simple. It scrapes the data displayed on https://www.worldometers.info/coronavirus/, saves it on a local database. You can later fetch it from there using the `/` endpoint. You can also lookup a particular country of your choosing with the `/countryname` endpoint.

For the first run, you must create the database and add its path to the .env file. SQLAlchemy is used to interact with the database, so Sqlite, MySQL and PostgreSQL should all work. Also, you will have to populate the DB. This can easily be done calling the `/update` endpoint from the browser. It can later be used to update the data. It will set off a background task to take care of it.

Lastly, to run the API locally can you use the following command:

`uvicorn app:app --reload --host 0.0.0.0 --port 8000`