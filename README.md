# single-elimination tournament
App for managing single-elimination tournaments created using REST API architecture.
The source code for this project can also be found on https://github.com/MaciPaci/single-elimination-tournament

### Features
- creating new tournament with defined date time and player count
- adding new players to the tournament
- automatically generated tournament bracket for each stage
- automatically determining winner of the tournament
- historical archive of past tournaments

### Installation guide for Windows
1. Make sure you have Python version 3.x installed. To do so open Command Prompt and type ```python --version```. If no Python version is installed download and install [newest version](https://www.python.org/downloads/).
2. Install virtualenv by typing in the Command Prompt ```pip3 install virtualenv```.
3. Unzip the project directory
4. Create new virtual environment ```py -m venv env```.
5. Activate created virtual environment ```.\env\Scripts\activate.bat```
6. Install required packages ```pip install -r requirements.txt```.
7. Create environment variable `export FLASK_APP=project`
8. Run the app ```flask run```.
9. Go to http://127.0.0.1:5000/.

### Pre-configuration 
The app comes with preconfigured database, containing user account with admin privileges.
To access the admin account simply login into the app using credentials:
 - email: `admin@example.com`
 - password: `admin`