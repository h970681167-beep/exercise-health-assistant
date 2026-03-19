import os
import json
from datetime import datetime
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from tools.feishu_bitable_tool import save_exercise_record, get_monthly_records
from graphs.state import ExerciseProcessingInput, ExerciseProcessingOutput


def exercise_processing_node(
    state: ExerciseProcessingInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ExerciseProcessingOutput:
    """
    title: 运动记录处理
    desc: 解析运动内容、计算热量、生成鼓励语，并保存到飞书多维表格
    integrations: 大语言模型, 飞书多维表格
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
        temperature=llm_config.get("temperature", 0.7),
        max_completion_tokens=llm_config.get("max_completion_tokens", 3000)
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
        exercise_type = result_data.get("exercise_type", "运动")
        duration = result_data.get("duration", 0)
        calories_burned = result_data.get("calories_burned", 0.0)
        description = result_data.get("description", "")
        encouragement_message = result_data.get("encouragement_message", "坚持运动，你真棒！")
    except json.JSONDecodeError:
        # 如果JSON解析失败，尝试提取JSON部分
        import re
        json_match = re.search(r'\{.*?\}', content_text, re.DOTALL)
        if json_match:
            try:
                result_data = json.loads(json_match.group())
                exercise_type = result_data.get("exercise_type", "运动")
                duration = result_data.get("duration", 0)
                calories_burned = result_data.get("calories_burned", 0.0)
                description = result_data.get("description", "")
                encouragement_message = result_data.get("encouragement_message", "坚持运动，你真棒！")
            except json.JSONDecodeError:
                exercise_type = "运动"
                duration = 0
                calories_burned = 0.0
                description = state.user_message
                encouragement_message = "坚持运动，你真棒！"
        else:
            exercise_type = "运动"
            duration = 0
            calories_burned = 0.0
            description = state.user_message
            encouragement_message = "坚持运动，你真棒！"

    # 从飞书表格获取本月记录，计算总时长
    try:
        monthly_records = get_monthly_records()

        # 计算总时长
        month_total_duration = int(duration)
        if isinstance(monthly_records, list):
            for record in monthly_records:
                if isinstance(record, dict):
                    record_fields = record.get("fields", {})
                    record_duration = record_fields.get("运动时长(分钟)", 0)
                    if isinstance(record_duration, (int, float)):
                        month_total_duration += int(record_duration)

        # 计算总热量（假设瘦牛肉热量约250千卡/100g）
        total_calories = float(calories_burned)
        if isinstance(monthly_records, list):
            for record in monthly_records:
                if isinstance(record, dict):
                    record_fields = record.get("fields", {})
                    record_calories = record_fields.get("燃烧热量(千卡)", 0.0)
                    if isinstance(record_calories, (int, float)):
                        total_calories += float(record_calories)

        meat_equivalent_grams = (total_calories / 250) * 100
        month_calories_equivalent = f"{meat_equivalent_grams:.0f}克瘦牛肉"
    except Exception as e:
        month_total_duration = int(duration)
        total_calories = float(calories_burned)
        meat_equivalent_grams = (total_calories / 250) * 100 if total_calories > 0 else 0
        month_calories_equivalent = f"{meat_equivalent_grams:.0f}克瘦牛肉"

    # 保存运动记录到飞书表格
    try:
        save_exercise_record(
            user_message=state.user_message,
            exercise_type=exercise_type,
            duration=duration,
            description=description,
            calories_burned=calories_burned,
            month_total_duration=month_total_duration,
            month_calories_equivalent=month_calories_equivalent,
            encouragement_message=encouragement_message
        )
    except Exception as e:
        print(f"保存记录失败: {e}")

    # 生成响应消息
    response_message = f"""运动记录已保存！
运动类型：{exercise_type}
运动时长：{duration}分钟
燃烧热量：{calories_burned:.1f}千卡

本月累计运动：{month_total_duration}分钟
本月消耗热量相当于：{month_calories_equivalent}

{encouragement_message}"""

    return ExerciseProcessingOutput(
        exercise_type=exercise_type,
        duration=duration,
        description=description,
        calories_burned=calories_burned,
        month_total_duration=month_total_duration,
        month_calories_equivalent=month_calories_equivalent,
        encouragement_message=encouragement_message,
        response_message=response_message
    )
