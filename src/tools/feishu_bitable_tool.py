"""
飞书多维表格工具类
用于存储和查询运动记录
"""

import requests
from functools import wraps
from cozeloop.decorator import observe
from coze_workload_identity import Client
from typing import List, Dict, Optional
from datetime import datetime


def get_access_token() -> str:
    """
    获取飞书多维表格的租户访问令牌
    """
    client = Client()
    access_token = client.get_integration_credential("integration-feishu-base")
    return access_token


class FeishuBitable:
    """
    飞书多维表格HTTP客户端
    """

    def __init__(self, base_url: str = "https://open.larkoffice.com/open-apis", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.access_token = get_access_token()

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}" if self.access_token else "",
            "Content-Type": "application/json; charset=utf-8",
        }

    @observe
    def _request(self, method: str, path: str, params: dict | None = None, json: dict | None = None) -> dict:
        try:
            url = f"{self.base_url}{path}"
            resp = requests.request(method, url, headers=self._headers(), params=params, json=json, timeout=self.timeout)
            resp_data = resp.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"FeishuBitable API request error: {e}")
        if resp_data.get("code") != 0:
            raise Exception(f"FeishuBitable API error: {resp_data}")
        return resp_data

    def add_record(
        self,
        app_token: str,
        table_id: str,
        record: dict,
    ) -> dict:
        """
        新增单条记录

        Args:
            app_token: 多维表格app_token
            table_id: 数据表table_id
            record: 记录数据，格式为 {"fields": {"字段名": 值, ...}}

        Returns:
            API响应结果
        """
        body = {"records": [record]}
        return self._request("POST", f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create", json=body)

    def search_records(
        self,
        app_token: str,
        table_id: str,
        page_size: int = 100,
        sort: Optional[list] = None,
    ) -> List[dict]:
        """
        查询所有记录

        Args:
            app_token: 多维表格app_token
            table_id: 数据表table_id
            page_size: 每页记录数，默认100
            sort: 排序条件，格式为 [{"field_name": "字段名", "desc": True/False}]

        Returns:
            记录列表
        """
        params = {"page_size": page_size}
        body = {}

        if sort:
            body["sort"] = sort

        result = self._request(
            "POST",
            f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/search",
            params=params,
            json=body
        )

        return result.get("data", {}).get("items", [])


def get_feishu_bitable() -> FeishuBitable:
    """获取飞书多维表格客户端实例"""
    return FeishuBitable()


def save_exercise_record(
    user_message: str,
    exercise_type: str,
    duration: int,
    description: str,
    calories_burned: float,
    month_total_duration: int,
    month_calories_equivalent: str,
    encouragement_message: str,
) -> bool:
    """
    保存运动记录到飞书多维表格

    Args:
        user_message: 用户原始消息
        exercise_type: 运动类型
        duration: 运动时长（分钟）
        description: 用户体验描述
        calories_burned: 燃烧热量（千卡）
        month_total_duration: 本月总时长（分钟）
        month_calories_equivalent: 本月总热量对应肉类
        encouragement_message: 鼓励语

    Returns:
        是否保存成功
    """
    try:
        # 从环境变量获取配置
        import os
        app_token = os.getenv("FEISHU_APP_TOKEN")
        table_id = os.getenv("FEISHU_EXERCISE_TABLE_ID")

        if not app_token or not table_id:
            raise ValueError("FEISHU_APP_TOKEN 或 FEISHU_EXERCISE_TABLE_ID 未配置")

        client = get_feishu_bitable()

        # 构建记录数据
        record = {
            "fields": {
                "用户消息": user_message,
                "运动类型": exercise_type,
                "运动时长(分钟)": duration,
                "燃烧热量(千卡)": calories_burned,
                "体验描述": description,
                "本月累计时长(分钟)": month_total_duration,
                "热量等价肉类": month_calories_equivalent,
                "鼓励语": encouragement_message,
                "记录时间": datetime.now().isoformat(),
            }
        }

        # 添加记录
        result = client.add_record(app_token, table_id, record)

        return result.get("code") == 0 and len(result.get("data", {}).get("records", [])) > 0

    except Exception as e:
        print(f"保存运动记录到飞书表格失败: {e}")
        return False


def get_monthly_records() -> List[dict]:
    """
    获取本月所有运动记录

    Returns:
        本月运动记录列表
    """
    try:
        import os
        from datetime import datetime

        app_token = os.getenv("FEISHU_APP_TOKEN")
        table_id = os.getenv("FEISHU_EXERCISE_TABLE_ID")

        if not app_token or not table_id:
            raise ValueError("FEISHU_APP_TOKEN 或 FEISHU_EXERCISE_TABLE_ID 未配置")

        client = get_feishu_bitable()

        # 查询所有记录，按记录时间降序排列
        records = client.search_records(
            app_token,
            table_id,
            page_size=100,
            sort=[{"field_name": "记录时间", "desc": True}]
        )

        # 筛选本月记录
        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)

        monthly_records = []
        for record in records:
            record_time_str = record.get("fields", {}).get("记录时间", "")
            if record_time_str:
                try:
                    record_time = datetime.fromisoformat(record_time_str)
                    if record_time >= month_start:
                        monthly_records.append(record)
                except ValueError:
                    continue

        return monthly_records

    except Exception as e:
        print(f"获取本月运动记录失败: {e}")
        return []
