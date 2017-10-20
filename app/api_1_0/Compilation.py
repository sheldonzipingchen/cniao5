# -*- coding: UTF-8 -*-
from flask import request, jsonify
from app.api_1_0 import api
from app.models import Compilation

__author__ = 'Ivan'


#PAGE_INDEX=0
PAGE_SIZE=10


@api.route('/compilations/<int:page_index>')
def page_compilations(page_index):

    #json = request.get_json()

    #page_index = json.get('page_index')

    paginate =Compilation.query.paginate(page_index,PAGE_SIZE)
    items = paginate.items
    total = paginate.total

    return  jsonify({'total':total,'page_size':PAGE_SIZE,'compilations':[c.to_Json() for c in items]})
