
import hashlib
import os

from backend import settings




def upload_hash_filename_wrapper(dir="",enable_date_dir=True):
    """ ### #django model field image 上传目录自定义

    Args:
        dir (str, optional): _description_. Defaults to "".
    """
    def hash_filename(instance, filename):
        # 读取文件内容并计算哈希值
        instance.image.open()
        contents = instance.image.read()
        hash_value = hashlib.md5(contents).hexdigest()

        # 获取文件扩展名
        _, ext = os.path.splitext(filename)

        if enable_date_dir:
            # 如果启用日期目录
            # 返回日期目录和哈希文件名
            return f"{settings.UPLOAD_DIR}/{dir}/{instance.created_at.strftime('%Y%m%d')}/{hash_value}{ext}"
        # 返回哈希文件名
        return f"{settings.UPLOAD_DIR}/{dir}/{hash_value}{ext}"
    # if runing or manage.py makemigrations
    if settings.RUNING:
        return hash_filename
    return settings.UPLOAD_DIR