# -*- coding: utf-8 -*-
from flask import g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import config

# Instancia de SQLAlchemy para usar con Flask-Migrate
db = SQLAlchemy()

# Engine manual (para modelos con SQLAlchemy puro)
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    echo=config.SQLALCHEMY_ECHO,
    future=True,
    pool_pre_ping=True,
)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True))
Base = declarative_base()

def get_db():
    if "db" not in g:
        g.db = SessionLocal()
    return g.db

def close_db(e=None):
    db_session = g.pop("db", None)
    if db_session is not None:
        db_session.close()

def init_db(app):
    db.init_app(app)
    app.teardown_appcontext(close_db)
