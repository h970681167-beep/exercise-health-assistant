import json
import requests
from coze_workload_identity import Client
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import FeishuSendMessageInput, FeishuSendMessageOutput


def get_feishu_webhook_url() -> str:
    """获取飞书webhook URL"""
    client = Client()
    feishu_credential = client.get_integration_credential("integration-feishu-message")
    webhook_key = json.loads(feishu_credential)["webhook_url"]
    return webhook_key


def feishu_send_node(
    state: FeishuSendMessageInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> FeishuSendMessageOutput:
    """
    title: 飞书消息发送
    desc: 通过飞书机器人发送消息
    integrations: 飞书消息
    """
    ctx = runtime.context

    try:
        # 获取webhook URL
        webhook_url = get_feishu_webhook_url()

        # 构建消息payload
        payload = {
            "msg_type": "text",
            "content": {
                "text": state.message
            }
        }

        # 发送消息
        response = requests.post(webhook_url, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                return FeishuSendMessageOutput(sent=True)
            else:
                return FeishuSendMessageOutput(sent=False)
        else:
            return FeishuSendMessageOutput(sent=False)

    except Exception as e:
        return FeishuSendMessageOutput(sent=False)
