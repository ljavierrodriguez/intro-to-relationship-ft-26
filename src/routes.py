from flask import Blueprint, request, jsonify
from models import db, User, Profile, New

api = Blueprint("api", __name__)

@api.route('/create-user', methods=['POST'])
def create_user():

    datos = request.json

    found = User.query.filter_by(username=datos.get('username')).first()

    if found:
        return jsonify({ "status": "fail", "msg": "User already exists"}), 422
    
    user = User()
    user.username = datos.get('username')
    profile = Profile()
    profile.biography = "Esto es una prueba"

    user.profile = profile

    db.session.add(user)
    db.session.commit()

    if user:
        return jsonify({"status": "success", "msg":"User created"}), 201
    else:
        return jsonify({"status": "fail", "msg": "User no created!"}), 400
    

@api.route('/create-new', methods=['POST'])
def create_new():

    datos = request.json
    
    create_new = New()
    create_new.title = datos.get('title')
    create_new.content = datos.get('content')
    create_new.users_id = datos.get('users_id')

    db.session.add(create_new)
    db.session.commit()

    if create_new:
        return jsonify({"status": "success", "msg":"New created"}), 201
    else:
        return jsonify({"status": "fail", "msg": "New no created!"}), 400
    


@api.route('/profile/<int:id>', methods=['GET'])
def get_profile(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({"status": "fail", "msg": "Profile not found"}), 404
    
    return jsonify({ "status": "success", "profile": user.serialize() }), 200


@api.route('/like', methods=['POST'])
def like_new():

    datos = request.json # news_id, users_id
    user = User.query.filter_by(id=datos.get('users_id')).first()
    new = New.query.filter_by(id=datos.get('news_id')).first()
    
    if new in user.likes:
        user.likes.remove(new)
    else: 
        user.likes.append(new)

    db.session.commit() 

    return jsonify(user.serialize()), 200
