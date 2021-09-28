from flask import Blueprint
from app.controllers.leads_controller import create_lead, delete_lead, list_leads, update_lead, delete_lead

bp = Blueprint('leads_bp', __name__, url_prefix='/lead')

bp.post('')(create_lead)
bp.get('')(list_leads)
bp.patch('')(update_lead)
bp.delete('')(delete_lead)
