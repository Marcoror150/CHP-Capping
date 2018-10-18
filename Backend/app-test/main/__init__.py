from flask import Blueprint

main = Blueprint('main', __name__)

# imports at the end of the file to prevent Flask context errors
from . import test 
