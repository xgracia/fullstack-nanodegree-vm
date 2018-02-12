FSND Project 3: Item Catalog
===

The following web app allows users to create, update, delete and view items in custom categories.

Demo web app:
---

- SSH into server @ IP `54.191.127.219` on port `2200`
- Demo is available at [http://udacity-fsnd-proj3.my.to/](http://udacity-fsnd-proj3.my.to/)
- Summary of software:
  - Python2
    - Flask
    - SQLAlchemy
    - oauth2client
    - Requests
  - Apache
    - mod_wsgi
  - Postgres
- Summary of configs:
  - Apache conf file modified to add `WSGIScriptAlias` pointing to web app
  - `myapp.wsgi` created to `import app` from `application.py`
  - Postgres user created with the permissions to related tables
  - `client_secret.json` updated to reflect new host / ip
- Resources used:
  - [Flask and WSGI](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/)
  - [Postgres user accounts](https://www.postgresql.org/docs/8.0/static/user-manag.html)
  - [Postgres GRANT](https://www.postgresql.org/docs/9.0/static/sql-grant.html)

Initial run:
---

- Run `db_setup.py` to set up the catalog database
- Run `db_populate.py` to populate the catalog database with data

Running the web app:
---

- Run `application.py` to start the web app on localhost port 5000
