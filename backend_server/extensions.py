from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource,request
from flask_marshmallow import Marshmallow
from flask import Blueprint,jsonify

db = SQLAlchemy()

ma = Marshmallow()