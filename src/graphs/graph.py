from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.exercise_processing_node import exercise_processing_node


# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("exercise_processing", exercise_processing_node, metadata={"type": "agent", "llm_cfg": "config/exercise_processing_cfg.json"})

# 设置入口点
builder.set_entry_point("exercise_processing")

# 添加边
builder.add_edge("exercise_processing", END)

# 编译图
main_graph = builder.compile()
