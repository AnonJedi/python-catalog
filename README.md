# Test project for present and manage products

### Preparing
All development was carried out on linux mint 17.3

#### Requirements
1) python 2.7
2) SQLite
    For installation and creation our databases run next commands in console from _path/to/project/application_ folder:
    ```
    sudo apt-get install sqlite3 libsqlite3-dev -y
    ```
    ```
    sqlite3 test.db
    ```
    After that actions we have created database _test.db_
    For exit from SQLite enter 
    ```
    .quit
    ```
3) virtualenv
    For installation virtualenv run:
    ```
    sudo apt-get install python-virtualenv -y
    ```
    Now go to folder with our project and run:
    ```
    virtualenv env
    ```
    For activation environment use 
    ```
    . env/bin/activate
    ```
    And for deactivation
    ```
    deactivate
    ```
    **!!!After that step all commands need to run under virtual environment!!!**
4) pip requirements
    For install all pip requirements use
    ```
    pip install requirements.txt
    ```

### Run the application
From project folder run:
```
python run_application.py
```