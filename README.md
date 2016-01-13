# drfunland
[![Build Status](https://travis-ci.org/Justin-W/drfunland.svg?branch=master)](https://travis-ci.org/Justin-W/drfunland)
[![Coverage Status](https://coveralls.io/repos/Justin-W/drfunland/badge.svg?branch=master&service=github)](https://coveralls.io/github/Justin-W/drfunland?branch=master)

Django REST Framework playground. A fun place to play around with [DRF](http://www.django-rest-framework.org/). Check out the project's [documentation](http://Justin-W.github.io/drfunland/).

# Prerequisites
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
- [postgresql](http://www.postgresql.org/) (e.g. "brew install postgresql")

## Heroku-related Prerequisites
Note: The following are only needed if you plan on deploying to heroku.
- [redis](http://redis.io/)
- [travis cli](http://blog.travis-ci.com/2013-01-14-new-client/)
- [heroku toolbelt](https://toolbelt.heroku.com/) (e.g. "brew install heroku-toolbelt")

# Project initialization

### CLI initialization/usage notes
Notes:
- Bash scripts for many common operations are located in the /scripts/ folder under the project root.
All of them are designed to be run from the directory they are located in.
- The /scripts/init.sh file can be modified to customize the location and name of the virtualenv.
- Warning: If you didn't install the prerequisites above, some of the scripts and run configurations may throw cryptic errors.
- IntelliJ Shared Run Configurations are also available for many of those Bash scripts.
- The examples and Bash scripts were created for Mac (OS X) development.
Alterations or equivalent implementations may be needed for use on Windows or Linux.
- The subsequent examples all assume the following paths are set correctly as environment variables.
However, these env variables are not required by the app itself, they are merely intended to make the CLI examples
in this readme more easily customizable.
```bash
REPO_PATH=~/dev/github/Justin-W/drfunland/drfunland
SCRIPTS_PATH=${REPO_PATH}/scripts
```

## One-time setup
Create and configure a virtualenv:

```bash
cd ${SCRIPTS_PATH}
bash venv.update.sh
```

### Install/update dependencies:

```bash
cd ${SCRIPTS_PATH}
bash venv.update.sh
```

### Create the database:
Note: Make sure your postgresql server is installed and running. e.g.:

```bash
postgres -D /usr/local/var/postgres
```

Then create the app's (empty) DB:
```bash
createdb drfunapp
```

### Initialize the git repository
Note: This is only necessary when creating a new git repo, not if you are cloning an existing one.
```
cd ${REPO_PATH}
git init
git remote add origin git@github.com:Justin-W/drfunland.git
```

### Migrate the DB, create a superuser, and run the server:
```bash
cd ${SCRIPTS_PATH} && source venv.activate.sh
#or: source ${VENV_PATH}/bin/activate

cd ${REPO_PATH}

#apply DB migrations
python drfunapp/manage.py migrate

#insert a superuser in the DB
python drfunapp/manage.py createsuperuser

#run the server
python drfunapp/manage.py runserver
```

## Heroku-related one-time setup
Note: you'll need to uncomment the "#deploy:" section of the '.travis.yml' file to enable automatic Heroku deployment.

### Create Servers
By default the included fabfile will setup three environments (as separate git remotes):

- dev -- The bleeding edge of development
- qa -- For quality assurance testing
- prod -- For the live application

Create these servers on Heroku with:

```bash
cd ${REPO_PATH}
source ${VENV_PATH}/bin/activate
fab init
```

### Automated Deployment
Deployment is handled via Travis. When builds pass Travis will automatically deploy that branch to Heroku. Enable this with:
```bash
travis encrypt $(heroku auth:token) --add deploy.api_key
```

# Running the app

### Run the tests
Run the project's test suite:

```bash
cd ${SCRIPTS_PATH}
bash fab.test.sh
```

### Run the server
Start the project's server:

```bash
cd ${SCRIPTS_PATH}
bash fab.serve.sh
```

### Browse the app
Assumes the app's server is already running (as described above):

```bash
#once running, access the app at:
open http://127.0.0.1:8000/api/v1/
open http://127.0.0.1:8000/admin/
```
