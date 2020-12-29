import json

from flask.json import jsonify
from flask_api import FlaskAPI

# export DATABASE_URL="postgres://marjanlukavyi:popqasef@localhost:5432/flask_api"

# local import
from app.models import db, User
from instance.config import app_config
from flask import request, abort

# initialize sql-alchemy

def create_app(config_name):
    from .models import Admin

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/admin/<int:id>/add_student/', methods=['POST'])
    def add_student(id):
        if request.method == 'POST':
            check_admin = Admin.query.filter_by(id=id).first()
            if(not check_admin):
                return {"ERROR": "немає такого адміна"}
            first_name = str(request.data.get('first_name', ''))
            last_name = str(request.data.get('last_name', ''))
            rating = str(request.data.get('rating', ''))
            email = str(request.data.get('email', ''))
            password = str(request.data.get('password', ''))
            if email and password:
                user = User(first_name=first_name, last_name=last_name, rating=rating, email=email, password=password)
                user.admins_students.append(check_admin)
                check_admin.admins_have_students.append(user)
                check_admin.save()
                user.save()

                response = jsonify({
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'rating': user.rating,
                    'email': user.email,
                    'password': user.password,
                    'admin_id': user.admins_students[0].id
                })
                response.status_code = 201
                return response
            else:
                return {"ERROR": "Wrong email/password"}


    @app.route('/students/', methods=['GET'])
    def users():
        # GET
        users = User.get_all()
        results = []
        for user in users:
            obj = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "rating": user.rating,
                "email": user.email,
                "password": user.password,
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/admins/', methods=['POST', 'GET'])
    def admins():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            email = str(request.data.get('email', ''))
            password = str(request.data.get('password', ''))
            if name:
                admin = Admin(name=name, email=email, password=password)
                admin.save()
                response = jsonify({
                    'id': admin.id,
                    'name': admin.name,
                    'date_created': admin.date_created,
                    'date_modified': admin.date_modified,
                    'email': admin.email,
                    'password': admin.password,
                })
                response.status_code = 201
                return response
        else:
            # GET
            admins = Admin.get_all()
            users = User.get_all()
            results = []

            for admin in admins:
                obj = {
                    'id': admin.id,
                    'name': admin.name,
                    'date_created': admin.date_created,
                    'date_modified': admin.date_modified,
                    'email': admin.email,
                    'password': admin.password,
                    'students': []
                }
                for student in admin.admins_have_students:
                    obj['students'].append({
                        "student name": student.first_name,
                        "email": student.email,
                        "rating": student.rating,
                        "id": student.id
                    })
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
    # User manipulation
    @app.route('/students/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def users_manipulation(id, **kwargs):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {
                       "message": "User id={} Not Found".format(id)
                   },404

        if request.method == 'DELETE':
            user.delete()
            return {
            "message": "user id={} deleted successfully".format(user.id)
         }, 200

        elif request.method == 'PUT':
            first_name = str(request.data.get('first_name', ''))
            user.first_name = first_name
            user.save()
            response = jsonify({
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'rating': user.rating,
                    'email': user.email,
                    'password': user.password
                })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'rating': user.rating,
                    'email': user.email,
                    'password': user.password
                })
            response.status_code = 200
            return response

    @app.route('/admins/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
        admin = Admin.query.filter_by(id=id).first()
        if not admin:
            return {
                       "message": "Admin id={} Not Found".format(id)
                   },404
        if request.method == 'DELETE':
            admin.delete()
            return {
            "message": "Admin id={} deleted successfully".format(admin.id)
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            admin.name = name
            admin.save()
            response = jsonify({
                    'id': admin.id,
                    'name': admin.name,
                    'date_created': admin.date_created,
                    'date_modified': admin.date_modified,
                    'email': admin.email,
                    'password': admin.password
                })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                    'id': admin.id,
                    'name': admin.name,
                    'date_created': admin.date_created,
                    'date_modified': admin.date_modified,
                    'email': admin.email,
                    'password': admin.password
                })
            response.status_code = 200
            return response
    return app
