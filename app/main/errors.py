# -*- coding: UTF-8 -*-
from flask import render_template, current_app, request, jsonify
from . import main

__author__ = 'Sheldon Chen'


@main.errorhandler(403)
def forbidden_page(error):
    current_app.logger.error(e.description)
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(error):
    """ 404 错误页面 """
    current_app.logger.error(error.description)
    if request.accept_mimetypes.accept_json and \
                 not request.accept_mimetypes.accept_html:
             response = jsonify({'error': 'not found'})
             response.status_code = 404
             return response

    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(error):
    """ 500 内部错误页面 """
    current_app.logger.error(error.description)
    return render_template('500.html'), 500
