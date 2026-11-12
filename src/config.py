"""应用配置模块。"""
import os
from pathlib import Path

# 项目根目录（src/）
BASE_DIR = Path(__file__).resolve().parent

# 数据库文件路径（可通过环境变量覆盖）
DATABASE = os.environ.get('SMS_DATABASE', str(BASE_DIR / 'sms.db'))

# 会话密钥
SECRET_KEY = os.environ.get('SMS_SECRET_KEY', 'dev-secret-key-change-me')

# 默认监听配置
HOST = '127.0.0.1'
PORT = 5000
