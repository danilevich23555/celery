import atexit
import os
import re
import uuid
from typing import Union

import pydantic
from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

app = Flask("server")
bcrypt = Bcrypt(app)
engine = create_engine('postgresql://app:1234@127.0.0.1:5432/netology')
Base = declarative_base()
Session = sessionmaker(bind=engine)


atexit.register(lambda: engine.dispose())




class ADS(Base):
    __tablename__ = "ads_table"
    id = Column(Integer, primary_key=True)
    heading = Column(String(100), nullable=False, unique=True)
    description = Column(String(200), nullable=False)
    create_time = Column(DateTime, server_default=func.now())
    owner = Column(String(200), nullable=False)


Base.metadata.create_all(engine)


class ADSViews(MethodView):
    def get(self, id: int):
        with Session() as session:
            query_id = session.query(ADS).get(id)
            return jsonify({
                'heading': query_id.heading,
                'owner': query_id.owner,
                'create_time': query_id.create_time.isoformat()
            })

    def post(self):
        json_data = request.json
        with Session() as session:
            ads = ADS(heading=json_data['heading'], description=json_data['description'], owner=json_data['owner'])
            session.add(ads)
            session.commit()
            return jsonify({
                'heading': ads.heading,
                'owner': ads.owner,
                'create_time': ads.create_time.isoformat()
            })

    def patch(self, id: int):
        json_data = request.json
        with Session() as session:
            i = session.query(ADS).get(id)
            for x, y in json_data.items():
                if x == 'heading':
                    i.heading = y
                else:
                    i.description = y
                session.add(i)
                session.commit()


    def delete(self, id: int):
        with Session() as session:
            i = session.query(ADS).filter(ADS.id == id).one()
            session.delete(i)
            session.commit()


app.add_url_rule('/ads/', view_func=ADSViews.as_view('create_ads'), methods=['POST'])
app.add_url_rule(
    "/ads/<int:id>/", view_func=ADSViews.as_view("get_ads"), methods=["GET"]
)
app.add_url_rule(
    "/ads/<int:id>/", view_func=ADSViews.as_view("patch_ads"), methods=["patch"]
)
app.add_url_rule(
    "/ads/<int:id>/", view_func=ADSViews.as_view("delete_ads"), methods=["DELETE"]
)


app.run(
    host='0.0.0.0',
    port=5000
)