import subprocess
import re
import os

def get_video_info(file_path):
    try:
        # 获取视频文件大小
        file_size = os.path.getsize(file_path)

        # 运行 ffmpeg 命令
        result = subprocess.run(['ffmpeg', '-i', file_path], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding='utf-8')
        output = result.stderr

        # 使用正则表达式提取视频时长
        duration_match = re.search(r"Duration: (\d+:\d+:\d+\.\d+)", output)
        if duration_match:
            duration = duration_match.group(1)
        else:
            duration = "N/A"

        # 使用正则表达式提取视频分辨率
        resolution_match = re.search(r"Stream.*Video.* (\d+x\d+)", output)
        if resolution_match:
            resolution = resolution_match.group(1)
        else:
            resolution = "N/A"

        return duration, resolution, file_size
    except UnicodeDecodeError as e:
        print(f"获取视频信息时出错: {e}")
        return None, None, None
    except Exception as e:
        print(f"获取视频信息时出错: {e}")
        return None, None, None

# 示例用法
file_path = "F:\\SUMMER\\新建文件夹\\3月19日(6).mp4"
duration, resolution, file_size = get_video_info(file_path)
print(f"视频时长: {duration}, 分辨率: {resolution}, 大小: {file_size} 字节")
