import os
from flask import (
    Flask,
    request,
    abort,
    jsonify
    )
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from models import (
    db_drop_and_create_all,
    setup_db,
    Collector,
    Set
    )
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # uncomment the following line to initialize the database

    # db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    #  Lego Sets
    #  ----------------------------------------------------------------

    @app.route('/sets', methods=['GET'])
    def get_sets():
        if not request.method == 'GET':
            abort(405)

        sets = Set.query.all()
        formatted_sets = [set.short() for set in sets]

        return jsonify({
            'success': True,
            'sets': formatted_sets
            }), 200

    @app.route('/sets-detail', methods=['GET'])
    @requires_auth('get:sets-detail')
    def get_sets_detail(token):
        if not request.method == 'GET':
            abort(405)

        sets = Set.query.all()
        formatted_sets = [set.long() for set in sets]

        return jsonify({
            'success': True,
            'sets': formatted_sets
            }), 200

    #  Create Sets
    #  ----------------------------------------------------------------

    @app.route('/sets', methods=['POST'])
    @requires_auth('post:sets')
    def create_set(token):
        if not request.method == 'POST':
            abort(405)

        data = request.get_json()
        id = data.get('id')
        name = data.get('name')
        year = data.get('year')
        pieces = data.get('pieces')

        try:
            set = Set(
                id=id,
                name=name,
                year=year,
                pieces=pieces
                )
            set.insert()

            return jsonify({
                'success': True,
                'created': set.short()
                }), 200

        except SQLAlchemyError:
            set.rollback()
            abort(422)

    #  Update Sets
    #  ----------------------------------------------------------------

    @app.route('/sets/<int:set_id>', methods=['PATCH'])
    @requires_auth('patch:sets')
    def update_set(token, set_id):
        if not request.method == 'PATCH':
            abort(405)

        set = Set.query.filter(Set.id == set_id).one_or_none()

        if set is None:
            abort(404)

        data = request.get_json()

        if 'name' in data:
            set.name = data.get('name')

        if 'year' in data:
            set.year = data.get('year')

        if 'pieces' in data:
            set.pieces = data.get('pieces')

        try:
            set.update()

            return jsonify({
                'success': True,
                'updated': set.long()
                })

        except SQLAlchemyError:
            set.rollback()
            abort(422)

    #  Delete Sets
    #  ----------------------------------------------------------------

    @app.route('/sets/<int:set_id>', methods=['DELETE'])
    @requires_auth('delete:sets')
    def delete_set(token, set_id):
        if not request.method == 'DELETE':
            abort(405)

        set = Set.query.filter(Set.id == set_id).one_or_none()

        if set is None:
            abort(404)

        try:
            set.delete()

            return jsonify({
                'success': True,
                'deleted': set_id
                })

        except SQLAlchemyError:
            set.rollback()
            abort(422)

    #  Collectors
    #  ----------------------------------------------------------------

    @app.route('/collectors', methods=['GET'])
    def get_collector():
        if not request.method == 'GET':
            abort(405)

        collectors = Collector.query.all()
        formatted_collectors = [collector.short() for collector in collectors]

        return jsonify({
            'success': True,
            'collectors': formatted_collectors
            }), 200

    @app.route('/collectors-detail', methods=['GET'])
    @requires_auth('get:collectors-detail')
    def get_collectors_detail(token):
        if not request.method == 'GET':
            abort(405)

        collectors = Collector.query.all()
        formatted_collectors = [collector.long() for collector in collectors]

        return jsonify({
            'success': True,
            'collectors': formatted_collectors
            }), 200

    #  Create Collectors
    #  ----------------------------------------------------------------

    @app.route('/collectors', methods=['POST'])
    @requires_auth('post:collectors')
    def create_collector(token):
        if not request.method == 'POST':
            abort(405)

        data = request.get_json()
        name = data.get('name')
        location = data.get('location')
        lego_ids = data.get('legos')

        if lego_ids is not None:
            legos = Set.query.filter(Set.id.in_(lego_ids)).all()
        else:
            legos = []

        try:
            collector = Collector(
                name=name,
                location=location,
                legos=legos
                )
            collector.insert()

            return jsonify({
                'success': True,
                'created': collector.long()
                }), 200

        except SQLAlchemyError:
            collector.rollback()
            abort(422)

    #  Update Collectors
    #  ----------------------------------------------------------------

    @app.route('/collectors/<int:collector_id>', methods=['PATCH'])
    @requires_auth('patch:collectors')
    def update_collector(token, collector_id):
        if not request.method == 'PATCH':
            abort(405)

        collector = Collector.query.filter(
            Collector.id == collector_id).one_or_none()

        if collector is None:
            abort(404)

        data = request.get_json()

        if 'name' in data:
            collector.name = data.get('name')

        if 'location' in data:
            collector.location = data.get('location')

        if 'legos' in data:
            lego_ids = data.get('legos')
            collector.legos = Set.query.filter(Set.id.in_(lego_ids)).all()

        try:
            collector.update()

            return jsonify({
                'success': True,
                'updated': collector.long()
                })

        except SQLAlchemyError:
            collector.rollback()
            abort(422)

    #  Delete Collectors
    #  ----------------------------------------------------------------

    @app.route('/collectors/<int:collector_id>', methods=['DELETE'])
    @requires_auth('delete:collectors')
    def delete_collector(token, collector_id):
        if not request.method == 'DELETE':
            abort(405)

        collector = Collector.query.filter(
            Collector.id == collector_id).one_or_none()

        if collector is None:
            abort(404)

        try:
            collector.delete()

            return jsonify({
                'success': True,
                'deleted': collector_id
                })

        except SQLAlchemyError:
            collector.rollback()
            abort(422)

    #  Error Handlers
    #  ----------------------------------------------------------------

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
                        "success": False,
                        "error": 401,
                        "message": "unauthorized"
                        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
                        "success": False,
                        "error": 405,
                        "message": "method not allowed"
                        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
                        "success": False,
                        "error": 500,
                        "message": "internal server error"
                        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
