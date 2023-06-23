from flask import render_template, jsonify

from . import app, db


@app.errorhandler(404)
def page_not_found(error):
    """Handler for site 404-errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler for site 500-errors."""
    db.session.rollback()
    return render_template('500.html'), 500


class InvalidAPIUsage(Exception):
    """Error class for API exceptions."""
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Handler for API exceptions."""
    return jsonify(error.to_dict()), error.status_code
