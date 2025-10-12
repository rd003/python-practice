from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_req_error(e):
        return jsonify({'error':'bad request'})
    
    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({'error':'not found'})
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error':'not found'})
    
    return app