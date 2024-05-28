import os
import re
import subprocess
from flask import Flask, render_template, send_from_directory, abort, url_for, request, redirect, send_file

app = Flask(__name__)

# 设置根目录，可以根据需要更改
ROOT_DIR = os.path.abspath("/SUMMER")

def get_video_info(file_path):
    app.logger.info(file_path)

    # 获取视频文件大小
    file_size = os.path.getsize(file_path)

    try:
        # Run ffmpeg command
        result = subprocess.run(['ffmpeg', '-i', file_path], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding='utf-8')
        output = result.stderr

        # Use regular expressions to extract video duration
        duration_match = re.search(r"Duration: (\d+:\d+:\d+)", output)
        if duration_match:
            duration = duration_match.group(1)
        else:
            duration = "N/A"

        # Use regular expressions to extract video resolution
        resolution_match = re.search(r"Stream.*Video.* (\d+x\d+)", output)
        if resolution_match:
            resolution = resolution_match.group(1)
        else:
            resolution = "N/A"

        return file_size, duration, resolution
    except UnicodeDecodeError as e:
        print(f"获取视频信息时出错: {e}")
        return None, None, None
    except Exception as e:
        print(f"获取视频信息时出错: {e}")
        return None, None, None

@app.route('/download/<path:subpath>')
def download(subpath):
    file_path = os.path.join(ROOT_DIR, subpath)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found', 404

@app.route('/delete/<path:subpath>', methods=['POST'])
def delete(subpath):
    if request.method == 'POST':
        file_path = os.path.join(ROOT_DIR, subpath)
        if os.path.exists(file_path):
            os.remove(file_path)
            return redirect(url_for('index', subpath=subpath.rsplit('/', 1)[0]))  # 删除成功后重定向到上一级目录
        else:
            return 'File not found', 404
    else:
        return 'Method not allowed', 405

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

        return render_template('index.html', path=subpath, dirs=dirs, files=files, os=os, get_video_info=get_video_info, ROOT_DIR=ROOT_DIR)

    # 如果路径既不是文件也不是目录，返回404
    abort(404)

@app.route('/preview/<path:subpath>')
def preview(subpath):
    current_path = os.path.join(ROOT_DIR, subpath)

    if not os.path.exists(current_path) or not os.path.isfile(current_path):
        abort(404)

    file_extension = os.path.splitext(current_path)[1].lower()

    if file_extension in ['.txt', '.md', '.py', '.log']:  # 支持的文本文件类型
        with open(current_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return render_template('preview.html', content=content, file_type='text')
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:  # 支持的图片文件类型
        return render_template('preview.html', file_url=url_for('index', subpath=subpath), file_type='image')

    abort(415)  # 不支持的文件类型

if __name__ == '__main__':
    # 修改 host 参数为 '0.0.0.0' 以允许局域网访问，端口为8080
    app.run(debug=True, host='0.0.0.0', port=8080)
