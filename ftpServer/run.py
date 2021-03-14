# -*- coding: utf-8 -*-
import os
import re
from urllib.parse import urlparse

from flask import Flask, render_template, url_for, redirect, send_file, abort, request
from werkzeug.datastructures import FileStorage

from . import utils
from .utils import RegexConverter

app = Flask(__name__)
app.url_map.converters['re'] = RegexConverter


@app.route("/")
def index():
    co = utils.get('static/')
    return render_template("index.html", **co)


@app.route('/<path:filename>')
def ico(filename):
    if r'.html' not in filename:
        return redirect('/static/config/' + filename)
    return render_template(filename)


@app.route("/static/")
def to_index():
    return redirect(url_for("index"))


@app.route('/static/<re(".+"):filename>')
def get(filename):
    file_path = urlparse(request.url).path[1:]
    if os.path.isdir(file_path):
        co = utils.get(file_path + '/')
        html = render_template("index.html", **co)
        return html
    elif r'.lnk' in file_path:
        # 真正的文件(夹) p
        if file_path.endswith('.lnk'):
            p = utils.pare_lnk(file_path)
        else:
            root_path = re.findall('^.*?\.lnk', file_path)[0]  # 根路径
            y_path = file_path.replace(root_path, '')  # 叶路径
            p = utils.pare_lnk(root_path) + y_path
        # 判断 p 是 文件还是文件夹
        if os.path.isdir(p):
            co = utils.get2(file_path, p)
            html = render_template("index.html", **co)
            return html

        elif os.path.exists(p):
            return send_file(p)
        else:
            abort(404)

    elif os.path.exists(file_path):
        return send_file('../' + file_path)
    else:
        abort(404)


@app.errorhandler(404)
def error_404(e):
    return render_template("404.html", er="您访问的页面去浪迹天涯了……"), 404


@app.route('/upload', methods=['POST'])
def upload():
    print(request.args)
    print(request.files)
    print(request.form)
    print(request.form.get('url'))
    try:
        file = request.files.get('file')  # type: FileStorage
        file_path = request.form.get('url')
        if r'.lnk' in file_path:
            root_path = re.findall('^.*?\.lnk', file_path)[0]  # 根路径
            y_path = file_path.replace(root_path, '')  # 叶路径
            p = utils.pare_lnk(root_path)
            file_path = p+y_path
        file.save(file_path + file.filename)
        print(file_path + file.filename)
    finally:
        return redirect('/' + request.form.get('url')[:-1])
