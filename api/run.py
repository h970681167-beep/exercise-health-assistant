"""
Vercel Serverless Function for /api/run endpoint
"""
import sys
import os
import json
from pathlib import Path

# 添加 src 目录到 Python 路径
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def handler(request):
    """
    Vercel Serverless Function handler
    
    Args:
        request: Vercel request object with body, method, headers
    
    Returns:
        Dict with statusCode, headers, body
    """
    # 解析请求体
    try:
        if isinstance(request.get('body'), str):
            body = json.loads(request.get('body', '{}'))
        else:
            body = request.get('body', {})
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Invalid JSON: {str(e)}"})
        }

    try:
        # 导入 service（延迟导入）
        from main import service
        from coze_coding_utils.runtime_ctx.context import new_context
        
        # 创建上下文
        ctx = new_context(method="run")
        
        # 调用 GraphService（同步调用）
        import asyncio
        result = asyncio.run(service.run(body, ctx))
        
        # 添加 run_id 到响应
        if isinstance(result, dict):
            result["run_id"] = ctx.run_id
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result, ensure_ascii=False)
        }
    
    except Exception as e:
        import traceback
        error_detail = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(error_detail, ensure_ascii=False)
        }
