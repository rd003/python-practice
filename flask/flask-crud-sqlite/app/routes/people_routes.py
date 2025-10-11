from flask import Blueprint, request, jsonify
from marshmallow import ValidationError


from ..extensions import db
from ..models import Person
from ..schemas import PersonSchema, PersonUpdateSchema

people_bp = Blueprint('people_bp',__name__)

person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
person_update_schema = PersonUpdateSchema()

@people_bp.get("/")
def get_people():
    people = Person.query.all()
    return jsonify(people_schema.dump(people))

@people_bp.get("/<int:id>")
def get_person(id):
    person = Person.query.get_or_404(id)
    return jsonify(person_schema.dump(person))

@people_bp.post("/")
def create_person():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    try:
        validated_data = person_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400    

    new_person = Person(
        first_name = validated_data['firstName'],
        last_name = validated_data['lastName']
    )

    try: 
        db.session.add(new_person)
        db.session.commit()
        return jsonify (new_person.to_dict()),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create person'}), 500

@people_bp.put("/<int:id>")
def update_person(id):
    if not request.is_json:
        return jsonify({'error':'Content-Type must be json/application'}),400

    person = Person.query.get_or_404(id)
    data = request.get_json()

    try:
        validated_data = person_update_schema.load(data)
    except ValidationError as err:
        return jsonify({'error':'Validation error', 'messages':err.messages}),400
    
    if 'firstName' in validated_data:
        person.first_name = validated_data['firstName']
    if 'lastName' in validated_data:
        person.last_name = validated_data['lastName']
    
    try:
       db.session.commit()
       return jsonify(person_schema.dump(person)),200
    except Exception as e:
        db.Session.rollback()
        return jsonify({'error':'Failed to update person'}),500   

@people_bp.delete("/<int:id>")
def delete_person(id):
    person = Person.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    return jsonify(),204