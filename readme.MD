# Django Based Notes App

## This App include CRUD Operations:
* Creation of New Note
* Update Existing Note
* Delete a note
* Get all notes for logged-in user.

## Authentication Functionality is also implemented.
Register an account.
Login/Logout to keep user specific notes.

## Running App Locally

For Building docker image of the app:

`docker build . -t notes-app-v0.0`

Run the docker image of the app

`docker run -network host notes-app-v0.0`

### Running unittest Locally
Notes app views tests : 
`python3 manage.py test notes.tests.test_views`

Note app models test: `python3 manage.py test notes.tests.test_models`