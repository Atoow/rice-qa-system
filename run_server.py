"""启动脚本：兼容单文件运行与 uvicorn 命令行"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backend.main import app
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
