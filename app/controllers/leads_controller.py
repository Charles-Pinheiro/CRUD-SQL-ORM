import re
from datetime import datetime

import sqlalchemy
from app.models.leads_model import Leads
from flask import current_app, request
from flask.json import jsonify
from psycopg2.errors import NotNullViolation
from sqlalchemy import desc


def create_lead():

    data = request.json

    if len(data) > 3:
        return {'message': 'Invalid fields.'}, 400

    for field, value in data.items():
        if type(value) != str:
            return {f'{field}': 'Has an invalid type.'}, 400

    if not re.fullmatch('\(\d{2}\)\d{5}-\d{4}', data['phone']):
        return {'message': 'Invalid phone number.'}, 400

    creation_date = datetime.today().strftime('%a, %d %b %Y %H:%M:%S %Z')
    last_visit = datetime.today().strftime('%a, %d %b %Y %H:%M:%S %Z')

    data['creation_date'] = creation_date
    data['last_visit'] = last_visit

    try:
        lead = Leads(**data)

        session = current_app.db.session

        session.add(lead)
        session.commit()

        return jsonify(lead), 201
        
    except sqlalchemy.exc.IntegrityError as e:

        if type(e.orig) == NotNullViolation:
            return {'message': str(e.orig).split('\n')[0]}, 400

        message = str(e.orig).split('\n')[1]
        return {'message': message[9:]}, 422
    
    except TypeError as e:
        return {'message': str(e)}, 400


def list_leads():

    leads_list = Leads.query.order_by(desc(Leads.visits)).all()
    if len(leads_list) == 0:
        return {'message': 'Empty list.'}, 404
    return jsonify(leads_list), 200


def update_lead():

    data = request.json
    email = data['email']

    lead = Leads.query.filter_by(email=email).first_or_404()
    
    lead.visits += 1
    lead.last_visit = datetime.today().strftime('%a, %d %b %Y %H:%M:%S %Z')
    
    current_app.db.session.commit()
    
    return '', 204


def delete_lead():

    data = request.json
    email = data['email']

    lead = Leads.query.filter_by(email=email).first_or_404()

    current_app.db.session.delete(lead)
    current_app.db.session.commit()

    return '', 204
