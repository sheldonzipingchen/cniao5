# -*- coding: UTF-8 -*-
from datetime import datetime

import sys
from flask import render_template, request, jsonify
from flask.ext.login import login_required

from app import cache
from app.dao.page_dao import PageMenuDao
from . import admin
from ..models import PageMenu



@admin.route("/page/menu.html")
@login_required
def page_menus():
    menus = PageMenuDao().find_by_type(1)
    return  render_template("admin/page/menu.html",menus=menus)




@admin.route("/page/menu/add",methods=["POST"])
@login_required
def page_menu_add():

    params = request.get_json()
    sort = params.get("sort")
    title = params.get("title")
    redirect_url = params.get("redirect_url")



    menu = PageMenu(title=title,
                    sort=sort,
                    redirect_url=redirect_url,
                    created_time=datetime.now(),
                    type=1
                    )
    PageMenuDao().save(menu)

    cache.clear()

    return jsonify(success=1,message=u'添加成功')




@admin.route("/page/menu/delete/<int:id>",methods=["POST"])
@login_required
def page_menu_delete(id):

    dao = PageMenuDao()
    menu = dao.get(id)
    dao.delete(menu)
    cache.clear()
    return jsonify(success=1, message=u'添加成功')
