# Install Requirements
- Python3
- Microsoft SQL Server

## Install virtual environments for Python3 and Windows
`
pip install virtualenv`

`pip install virtualenvwrapper-win`

## Creating and using a virtual environment
Creating an environment:

`mkvirtualenv chp-webserver`

Switch to the newly created environment:

`workon chp-webserver`

Install the remainder of application dependencies on the virtual environments:

`pip install -r requirements.txt`