"""
Vercel Python Application Entry Point
使用 serverless-http 包装 FastAPI 应用
"""
from main import app
import serverless_http

# 使用 serverless-http 包装 FastAPI 应用，使其能在 Vercel 上运行
handler = serverless_http(app)
