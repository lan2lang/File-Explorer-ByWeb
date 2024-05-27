import os
from waitress import serve
from flask import Flask, render_template, request, send_from_directory, abort

app = Flask(__name__)

# 设置根目录，可以根据需要更改
ROOT_DIR = os.path.abspath("/SUMMER")

@app.route('/')
@app.route('/<path:subpath>')
def index(subpath=''):
    # 获取当前目录路径
    current_path = os.path.join(ROOT_DIR, subpath)

    # 检查路径是否存在
    if not os.path.exists(current_path):
        abort(404)

    # 如果是文件，则直接返回文件内容
    if os.path.isfile(current_path):
        return send_from_directory(os.path.dirname(current_path), os.path.basename(current_path))

    # 如果是目录，则列出目录内容
    if os.path.isdir(current_path):
        files = []
        dirs = []
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            else:
                files.append(item)

        return render_template('index.html', path=subpath, dirs=dirs, files=files)

    # 如果路径既不是文件也不是目录，返回404
    abort(404)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
