# -*- coding: utf-8 -*-
from flask import Flask
from flask_migrate import Migrate
from app.extensions import db
from app import create_app

app = create_app()
migrate = Migrate(app, db)
