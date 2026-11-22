# Airport automatization softwate server
## running server
### create python virtual environment
```bash
python -m env .env
```
### activate environment
```bash
source .venv/bin/activate
```
on linux, *BSD, MacOS
and
```cmd
.venv\Scripts\activate.bat
```
on Windows (cmd)
### install dependencies
you can see them in [requirements.txt](./requirements.txt) and install with
```bash
pip install -r requirements.txt
```
note that after running this command only pure-python version of psycopg will be installed, which may affect performance. and it also requires PostgreSQL client libraries to be installed.

so instead consider installing psycopg[c] (requieres client libraries alongside with build tools) or psycopg[binary] (which requiers neither client libraries nor build tools).

see psycopg's [installation guide](https://www.psycopg.org/psycopg3/docs/basic/install.html) for more information.
### create PostgreSQL database
you can just do `create database airport;` and use it wiht postgres user or for better security additionaly create separate user with limited rights
### set up .env file
create *_.env_* file in project's root
#### add database URI to .env file
put something like
```bash
DATABASE_URL="postgresql+psycopg://user:password@server:port/db_name"
```
in it
#### generate JWK (key for tokens) and add to the .env file
you can generate token using openssl:
```bash
openssl rand -base64 32
```
this command will generate key with length of 32 bytes.
then put it in file like that:
```bash
JWK="eZjTSZSJ+Lubc9XGwB7+aurOsJQrffFUbj/P+ApOqjk="
```
#### add username and password for first admin account
```bash
ADMIN_NAME="admin"
ADMIN_PWD="12345"
```
this account will only be created if its name is not taken
### run the module
run
```bash
python -m app.main
```
