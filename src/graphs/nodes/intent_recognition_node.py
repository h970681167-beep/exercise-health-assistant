import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import IntentRecognitionInput, IntentRecognitionOutput


def intent_recognition_node(
    state: IntentRecognitionInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> IntentRecognitionOutput:
    """
    title: 意图识别
    desc: 识别用户的意图是设置提醒还是记录运动，并提取关键信息
    integrations: 大语言模型
    """
    ctx = runtime.context

    # 读取配置文件
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    # 使用jinja2模板渲染提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({"user_message": state.user_message})

    # 初始化LLM客户端
    client = LLMClient(ctx=ctx)

    # 构建消息
    messages = [
        SystemMessage(content=sp),
        HumanMessage(content=user_prompt_content)
    ]

    # 调用大模型
    response = client.invoke(
        messages=messages,
        model=llm_config.get("model", "doubao-seed-1-8-251228"),
        temperature=llm_config.get("temperature", 0.3),
        max_completion_tokens=llm_config.get("max_completion_tokens", 2000)
    )

    # 安全提取文本内容
    content_text = ""
    if isinstance(response.content, str):
        content_text = response.content.strip()
    elif isinstance(response.content, list):
        if response.content and isinstance(response.content[0], str):
            content_text = " ".join(response.content).strip()
        else:
            text_parts = []
            for item in response.content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            content_text = " ".join(text_parts).strip()

    # 解析JSON响应
    try:
        result_data = json.loads(content_text)
        intent = result_data.get("intent", "")
        extracted_data = result_data.get("extracted_data", {})
    except json.JSONDecodeError:
        # 如果JSON解析失败，尝试提取JSON部分
        import re
        json_match = re.search(r'\{.*?\}', content_text, re.DOTALL)
        if json_match:
            try:
                result_data = json.loads(json_match.group())
                intent = result_data.get("intent", "")
                extracted_data = result_data.get("extracted_data", {})
            except json.JSONDecodeError:
                # 默认为运动记录
                intent = "exercise"
                extracted_data = {}
        else:
            intent = "exercise"
            extracted_data = {}

    return IntentRecognitionOutput(
        intent=intent,
        extracted_data=extracted_data
    )
