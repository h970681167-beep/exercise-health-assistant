from datetime import datetime
from typing import Optional
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from storage.database.supabase_client import get_supabase_client
from graphs.state import ReminderProcessingInput, ReminderProcessingOutput


def reminder_processing_node(
    state: ReminderProcessingInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ReminderProcessingOutput:
    """
    title: 定时提醒处理
    desc: 将用户的提醒任务保存到数据库
    integrations: Supabase
    """
    ctx = runtime.context

    try:
        # 获取Supabase客户端
        client = get_supabase_client()

        # 从 state 中获取提醒时间，如果没有则设置为1小时后
        remind_time_str = state.remind_time if state.remind_time else ""
        remind_time: Optional[datetime] = None

        if remind_time_str:
            try:
                remind_time = datetime.fromisoformat(remind_time_str)
            except ValueError:
                # 如果解析失败，设置为当前时间+1小时
                from datetime import timedelta
                remind_time = datetime.now() + timedelta(hours=1)
        else:
            # 默认设置为1小时后
            from datetime import timedelta
            remind_time = datetime.now() + timedelta(hours=1)

        # 插入提醒记录
        reminder_data = {
            'user_message': state.user_message,
            'remind_time': remind_time.isoformat(),
            'sent': False
        }

        response = client.table('reminders').insert(reminder_data).execute()

        if response.data:
            return ReminderProcessingOutput(
                reminder_saved=True,
                response_message=f"已为你设置提醒：{state.user_message}\n提醒时间：{remind_time.strftime('%Y-%m-%d %H:%M')}\n我会通过飞书通知你！"
            )
        else:
            return ReminderProcessingOutput(
                reminder_saved=False,
                response_message="抱歉，设置提醒失败，请稍后重试。"
            )

    except Exception as e:
        return ReminderProcessingOutput(
            reminder_saved=False,
            response_message=f"设置提醒时发生错误：{str(e)}"
        )
