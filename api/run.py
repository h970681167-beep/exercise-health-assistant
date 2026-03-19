"""
Vercel Serverless Function for /api/run endpoint
"""
import sys
import os
from pathlib import Path

# 添加 src 目录到 Python 路径
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

import json
from fastapi import Request
from starlette.responses import JSONResponse

# 导入 main.py 中的 app
from main import app, service
from coze_coding_utils.runtime_ctx.context import new_context, Context

async def handler(request):
    """
    Vercel Serverless Function handler
    """
    # 解析请求体
    try:
        body = await request.json()
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid JSON: {str(e)}"}
        )

    # 创建上下文
    ctx = new_context(method="run")
    
    try:
        # 调用 GraphService
        result = await service.run(body, ctx)
        
        # 添加 run_id 到响应
        if isinstance(result, dict):
            result["run_id"] = ctx.run_id
        
        return JSONResponse(content=result)
    
    except Exception as e:
        import traceback
        error_detail = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        return JSONResponse(
            status_code=500,
            content=error_detail
        )

# Vercel 会自动调用这个函数
async def main_handler(request):
    return await handler(request)

# 兼容 Vercel 的导出方式
handler_v2 = main_handler
