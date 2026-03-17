from typing import Optional
from pydantic import BaseModel, Field


class GlobalState(BaseModel):
    """全局状态定义"""
    user_message: str = Field(..., description="用户输入的消息")
    intent: str = Field(default="", description="意图识别结果：reminder（提醒）/exercise（运动记录）")

    # 提醒相关
    remind_time: str = Field(default="", description="提醒时间（ISO格式）")
    reminder_saved: bool = Field(default=False, description="提醒是否已保存")

    # 运动记录相关
    exercise_type: str = Field(default="", description="运动类型")
    duration: int = Field(default=0, description="运动时长（分钟）")
    calories_burned: float = Field(default=0.0, description="燃烧热量（千卡）")
    month_total_duration: int = Field(default=0, description="本月总时长（分钟）")
    month_calories_equivalent: str = Field(default="", description="本月总热量对应肉类")
    encouragement_message: str = Field(default="", description="鼓励语")

    # 响应
    response_message: str = Field(default="", description="返回给用户的响应消息")


class GraphInput(BaseModel):
    """工作流输入"""
    user_message: str = Field(..., description="用户输入的消息")


class GraphOutput(BaseModel):
    """工作流输出"""
    response_message: str = Field(..., description="返回给用户的响应消息")


# ===== 意图识别节点 =====

class IntentRecognitionInput(BaseModel):
    """意图识别节点输入"""
    user_message: str = Field(..., description="用户输入的消息")


class IntentRecognitionOutput(BaseModel):
    """意图识别节点输出"""
    intent: str = Field(..., description="意图识别结果：reminder（提醒）/exercise（运动记录）")
    extracted_data: dict = Field(default={}, description="提取的数据（提醒时间、运动类型、时长等）")


# ===== 定时提醒处理节点 =====

class ReminderProcessingInput(BaseModel):
    """定时提醒处理节点输入"""
    user_message: str = Field(..., description="用户消息内容")
    remind_time: str = Field(default="", description="提醒时间（ISO格式字符串）")
    intent: str = Field(default="", description="意图类型")


class ReminderProcessingOutput(BaseModel):
    """定时提醒处理节点输出"""
    reminder_saved: bool = Field(..., description="提醒是否已保存")
    response_message: str = Field(..., description="响应消息")


# ===== 运动记录处理节点 =====

class ExerciseProcessingInput(BaseModel):
    """运动记录处理节点输入"""
    user_message: str = Field(..., description="用户消息内容")


class ExerciseProcessingOutput(BaseModel):
    """运动记录处理节点输出"""
    exercise_type: str = Field(..., description="运动类型")
    duration: int = Field(..., description="运动时长（分钟）")
    calories_burned: float = Field(..., description="燃烧热量（千卡）")
    month_total_duration: int = Field(..., description="本月总时长（分钟）")
    month_calories_equivalent: str = Field(..., description="本月总热量对应肉类")
    encouragement_message: str = Field(..., description="鼓励语")
    response_message: str = Field(..., description="响应消息")


# ===== 飞书消息发送节点 =====

class FeishuSendMessageInput(BaseModel):
    """飞书消息发送节点输入"""
    message: str = Field(..., description="要发送的消息内容")


class FeishuSendMessageOutput(BaseModel):
    """飞书消息发送节点输出"""
    sent: bool = Field(..., description="是否发送成功")
