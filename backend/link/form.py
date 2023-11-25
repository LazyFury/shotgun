from django.forms import ModelForm
from .models import QRCode


class QRCodeForm(ModelForm):
    class Meta:
        model = QRCode
        exclude = []
        labels = {
            "originUrl": "原始链接",
            "type": "类型",
        }
        help_texts = {
            "originUrl": "请输入原始链接",
            "type": "请选择类型",
        }
        error_messages = {
            "originUrl": {
                "max_length": "链接过长",
                "required": "请输入原始链接",
            },
            "type": {
                "max_length": "类型过长",
                "required": "请选择类型",
            },
        }
