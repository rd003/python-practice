from flask import jsonify
from marshmallow import ValidationError

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400


    @app.errorhandler(404)
    def handle_not_found(err):
        return jsonify({'error': 'Resource not found'}), 404


    @app.errorhandler(500)
    def handle_internal_server_error(err):
        return jsonify({'error': 'Internal server error'}), 500
