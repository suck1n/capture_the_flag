Capture The Flag Website for students to have some fun while learning some basic hacking methods.

# Environment Setup
It can be run on either Windows or Linux. But only Linux has been tested.
## Requirements
* [NodeJS](#nodejs-installation)
* [Python 3](#python-3-installation)
* [SQLite 3](#sqlite-3-installation)

### NodeJS Installation
You can either download NodeJS with your package manager or download [nvm](https://github.com/nvm-sh/nvm#install--update-script) (node version manager).
I recommend using `nvm`, since it will allow you to have multiple NodeJS version installed and handle them with ease.

### Python 3 Installation
Download Python 3 via the package manager of your choice (example: `sudo apt install python3`).

### SQLite 3 Installation
Install SQLite 3 via the package manager of your choice. (example: `sudo apt install sqlite3`)

# Server Setup
## NPM Dependencies
You need to install all dependencies by executing the command `npm install` inside the project root directory.

## Session Password
For the encryption of the session cookies, you need to edit the `.env.local` file in the root directory.
Replace the placeholder `[password]` with a strong password (at least 32 characters long).

## Create the Database
Inside the project root directory you need to create a database file named `capture_the_flag.db`. 
After that, create all necessary tables inside the database. You can achieve that via the command `cat database.sql | sqlite3 capture_the_flag.db`

## Finalize the Flag system
For the capture the flag system to work, you need to edit the path to the newly created sqlite3 database file inside the `flag` program, use the absolute path.
After you edited it, you need to move it from the project root directory into the `/bin/` folder and mark it as an executable (if it is not already).

# Running the Server

## NextJS
### Development
If you want to test the application, you can run it with the command `npm run dev`. It should start on `0.0.0.0:3000`.

### Production
If you want to run the production server, just run the command `npm run prod`. It should build the project and
run it on `0.0.0.0:80`.

## Task Server
You can execute any task program with the command `python3 app.py`. The server should then listen on `0.0.0.0:5000` 
for Task0, 5001 for Task1, 5002 for Task2 etc.
Some tasks need an "Admin", who needs to be hacked. These programs can be started with `python3 admin.py`
and will listen on `127.0.0.1:6000` (6005 for Task5, ...). The admins programs can not and should not be reached from outside,
they should only be reached from the computer itself.