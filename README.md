# backend_project_v1

## instructions to get running ##

* [Install python 2.7](https://www.python.org/download/releases/2.7/)
* [Install pip](https://pip.pypa.io/en/stable/installing/) (looks like this ships with python now)
* [Download and install mySQL server](https://dev.mysql.com/downloads/mysql/)
* Start MySQL server on [windows](https://dev.mysql.com/doc/refman/8.0/en/windows-start-command-line.html) or [linux / mac](https://coolestguidesontheplanet.com/start-stop-mysql-from-the-command-line-terminal-osx-linux/)
* [Use pip to install pipenv (pip install pipenv)](https://pypi.org/project/pipenv/)
* Pull a copy of the project from this repository
* whilst still in cmd prompt | terminal and the new directory:
   1. set | export FLASK_APP=autoapp  
   2. set | export FLASK_ENV=development  
   3. set | export FLASK_DEBUG=1 (*only if you would like pretty JSON returned)  
   4. pipenv install  
   5. pipenv run flask run  
