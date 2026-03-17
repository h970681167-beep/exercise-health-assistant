## 项目概述
- **名称**: 智能提醒与运动健康助手
- **功能**: 对话式AI系统，支持定时提醒设置和运动记录分析，通过飞书推送提醒，自动计算运动热量并生成鼓励语

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| intent_recognition | `nodes/intent_recognition_node.py` | agent | 意图识别，判断用户是设置提醒还是记录运动 | reminder→reminder_processing<br>exercise→exercise_processing | `config/intent_recognition_cfg.json` |
| reminder_processing | `nodes/reminder_processing_node.py` | task | 将提醒任务保存到数据库 | - | - |
| exercise_processing | `nodes/exercise_processing_node.py` | agent | 解析运动内容、计算热量、生成鼓励语 | - | `config/exercise_processing_cfg.json` |
| feishu_send | `nodes/feishu_send_node.py` | task | 发送飞书消息 | - | - |
| route_based_on_intent | `graph.py` | condition | 根据意图路由到不同处理节点 | "处理提醒"→reminder_processing<br>"处理运动"→exercise_processing | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支)

## 子图清单
无子图

## 技能使用
- 节点 `intent_recognition` 使用 大语言模型
- 节点 `exercise_processing` 使用 大语言模型 + Supabase
- 节点 `reminder_processing` 使用 Supabase
- 节点 `feishu_send` 使用 飞书消息

## 数据库表结构
### reminders（提醒任务表）
- id: 主键
- user_message: 用户消息内容
- remind_time: 提醒时间
- sent: 是否已发送
- created_at: 创建时间

### exercise_records（运动记录表）
- id: 主键
- user_message: 用户消息内容
- exercise_type: 运动类型
- duration: 运动时长（分钟）
- description: 用户描述/体验
- calories_burned: 燃烧热量（千卡）
- month_total_duration: 本月总时长（分钟）
- month_calories_equivalent: 本月总热量对应肉类
- encouragement_message: 鼓励语
- created_at: 创建时间

## 使用说明
### 提醒功能
发送消息示例：
- "明天早上9点提醒我开会"
- "提醒我下午3点喝水"
- "下周三下午5点提醒我取快递"

系统会：
1. 识别提醒意图
2. 解析提醒时间
3. 保存到数据库
4. 定时通过飞书推送提醒

### 运动记录功能
发送消息示例：
- "今天跑了5公里，感觉还不错"
- "游泳了40分钟，感觉轻松"
- "健身1小时，有点累"

系统会：
1. 识别运动意图
2. 解析运动类型、时长、体验
3. 计算燃烧热量
4. 统计本月累计运动
5. 生成鼓励语
6. 保存到数据库

## 工作流程
```
用户消息 → 意图识别节点 → 条件分支
                            ├─ 提醒 → 定时提醒处理节点 → 结束
                            └─ 运动 → 运动记录处理节点 → 结束
```
