from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput,
    IntentRecognitionInput,
    IntentRecognitionOutput,
    ReminderProcessingInput,
    ReminderProcessingOutput,
    ExerciseProcessingInput,
    ExerciseProcessingOutput
)
from graphs.nodes.intent_recognition_node import intent_recognition_node
from graphs.nodes.reminder_processing_node import reminder_processing_node
from graphs.nodes.exercise_processing_node import exercise_processing_node
from graphs.nodes.feishu_send_node import feishu_send_node


def route_based_on_intent(state: GlobalState) -> str:
    """
    title: 根据意图路由
    desc: 根据意图识别结果路由到不同的处理节点
    """
    if state.intent == "reminder":
        return "处理提醒"
    elif state.intent == "exercise":
        return "处理运动"
    else:
        return "处理运动"


# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("intent_recognition", intent_recognition_node, metadata={"type": "agent", "llm_cfg": "config/intent_recognition_cfg.json"})
builder.add_node("reminder_processing", reminder_processing_node)
builder.add_node("exercise_processing", exercise_processing_node, metadata={"type": "agent", "llm_cfg": "config/exercise_processing_cfg.json"})

# 设置入口点
builder.set_entry_point("intent_recognition")

# 添加条件分支
builder.add_conditional_edges(
    source="intent_recognition",
    path=route_based_on_intent,
    path_map={
        "处理提醒": "reminder_processing",
        "处理运动": "exercise_processing"
    }
)

# 添加后续边
builder.add_edge("reminder_processing", END)
builder.add_edge("exercise_processing", END)

# 编译图
main_graph = builder.compile()
