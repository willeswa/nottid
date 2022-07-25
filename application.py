import os
from threading import Thread
from models import application
from models import Profile, db, JournalEntry
from flask import jsonify, request, Response
from sqlalchemy import exc
from cronjob import start_schedule

application = application

# Start the background thread for scheduling emails
daemon = Thread(target=start_schedule, daemon=True, name="email_entries")
daemon.start()

# Prep the database
# db.drop_all()
db.create_all()

# Get all entries endpoint
@application.route('/nottid/entries', methods=['GET'])
def get_entries():
    token = request.headers.get('Authorization')
    if token == None:
        return jsonify({'error': 'Authentication required!'}), 401

    try:
        auth_token = Profile.decode_token(token)
        users_entries = db.session.query(JournalEntry).filter_by(author_id=auth_token)

        entries = []
        for entry in users_entries:
            author = db.session.query(Profile).filter_by(author_id=entry.author_id).first()
            entries.append({"entry": entry.serialize(), "author": author.serialize()})
            
        return jsonify({'entries': entries}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401
    


# Create entry endpoint
@application.route('/nottid/entries', methods=['POST'])
def create_entry():
    auth = request.headers.get('Authorization')
    
    if auth == None:
        return jsonify({'error': 'Authentication required!'}), 401

    try:
        auth_token = Profile.decode_token(auth)
        body = request.get_json()
        text = body.get('text')

        if text == None or text == "":
            return jsonify({'error': 'A jornal must contain text'}), 400
        
        db.session.add(JournalEntry(text=body['text'], author_id=auth_token))
        db.session.commit()
        return jsonify({'message': 'Successly created entry'}), 201

    except exc.SQLAlchemyError as er:
        return jsonify({'error': str(er)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 401


# Create account endpoint
@application.route('/nottid/register', methods=['POST'])
def create_profile():

    body = request.get_json()
    email = body.get('email')
    password = body.get('password')
    username = body.get('username')

    if(email == None or email == ""): 
        return jsonify({'error': 'Please provide a valid email'}), 400

    if(password == None or password == ""): 
        return jsonify({'error': 'Please provide a valid password'}), 400

    if(username == None or username == ""): 
        return jsonify({'error': 'Please provide a valid username'}), 400

    try:
        user = Profile(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_token(user.author_id)
        return jsonify({'message': 'Successfuly created account', 'user': user.serialize(), 'token': auth_token})
    except exc.IntegrityError:
        return jsonify({'error': "Email already registered."}), 403
    except exc.SQLAlchemyError as e:
        return jsonify({'error': e})
    

# Login endpoint
@application.route('/nottid/login', methods=['POST'])
def login_profile():
    body = request.get_json()
    email = body.get('email')
    password = body.get('password')

    if(email == None or email == ""): 
        return jsonify({'error': 'Please provide a valid email'}), 400

    if(password == None or password == ""): 
        return jsonify({'error': 'Please provide a valid password'}), 400

    try:
        user = Profile.query.filter_by(
            email=email,
            password=password
        ).first()
        if user == None:
            return jsonify({'error': 'No user with that email!'}), 401

        auth_token = user.encode_token(user.author_id)
        return jsonify({'message': 'Login successful', 'user': user.serialize(), 'token': auth_token}), 200


    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    if os.environ.get("DEVELOPMENT"):
        application.debug = True
        application.run()
    else:
        application.debug = False
        application.run()