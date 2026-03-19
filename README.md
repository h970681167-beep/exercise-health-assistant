# 🏃 运动健康助手 - 云端部署版

智能运动记录助手，基于LangGraph工作流，使用飞书多维表格存储数据。

## ✨ 功能特点

- 🤖 **智能解析**：AI自动识别运动类型、时长、体验
- 📊 **热量计算**：根据运动类型自动计算燃烧热量
- 📈 **数据统计**：自动统计本月累计运动时长
- 🥩 **热量换算**：将热量转换为食物（瘦牛肉）重量
- 💪 **鼓励语**：生成个性化鼓励，激励坚持运动
- 📱 **云端存储**：数据存储在飞书多维表格，多端同步
- ☁️ **云端部署**：部署到Vercel，手机随时可用

## 🚀 快速开始

### 1. 创建飞书多维表格

在飞书中创建多维表格，添加以下字段：

| 字段名 | 字段类型 | 说明 |
|--------|---------|------|
| 用户消息 | 文本 | 用户原始输入 |
| 运动类型 | 文本 | 跑步/游泳/健身等 |
| 运动时长(分钟) | 数字 | 运动时长 |
| 燃烧热量(千卡) | 数字 | 计算的热量 |
| 体验描述 | 文本 | 用户的感受 |
| 本月累计时长(分钟) | 数字 | 本月总时长 |
| 热量等价肉类 | 文本 | 对应多少克肉 |
| 鼓励语 | 文本 | AI生成的鼓励 |
| 记录时间 | 日期时间 | 创建时间 |

### 2. 获取飞书表格配置

1. 打开创建的多维表格
2. 复制URL中的 `app_token`（在 `base/` 和 `/table/` 之间）
3. 点击"更多" → "高级" → "数据表ID"，复制 `table_id`

### 3. 部署到 Vercel

#### 方法一：使用 Vercel CLI（推荐）

```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录 Vercel
vercel login

# 部署项目
cd /path/to/your/project
vercel

# 配置环境变量
# FEISHU_APP_TOKEN: 你复制的app_token
# FEISHU_EXERCISE_TABLE_ID: 你复制的table_id
```

#### 方法二：通过 Vercel 网页端

1. 将代码推送到 GitHub
2. 登录 [Vercel](https://vercel.com)
3. 点击 "New Project"
4. 导入你的 GitHub 仓库
5. 在 "Environment Variables" 中添加：
   - `FEISHU_APP_TOKEN`: 你的飞书表格app_token
   - `FEISHU_EXERCISE_TABLE_ID`: 你的飞书表格table_id
6. 点击 "Deploy"

### 4. 使用方式

部署成功后，你会获得一个 Vercel 分配的URL（如 `https://your-project.vercel.app`）。

你可以通过以下方式使用：

#### 方式1：通过 API 调用

```bash
curl -X POST https://your-project.vercel.app/api/run \
  -H "Content-Type: application/json" \
  -d '{"user_message": "今天跑了5公里，感觉还不错"}'
```

#### 方式2：集成到飞书机器人

在飞书机器人中，将用户消息转发到你的 Vercel API。

## 📦 项目结构

```
├── src/
│   ├── graphs/
│   │   ├── state.py              # 状态定义
│   │   ├── graph.py              # 主图编排
│   │   └── nodes/
│   │       └── exercise_processing_node.py  # 运动处理节点
│   └── tools/
│       └── feishu_bitable_tool.py  # 飞书表格工具
├── config/
│   └── exercise_processing_cfg.json  # 大模型配置
├── requirements.txt               # Python依赖
├── vercel.json                    # Vercel配置
└── .env.example                   # 环境变量示例
```

## 🧪 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的配置

# 测试工作流
python -m src.main --test "今天跑了5公里，感觉还不错"
```

## 💡 使用示例

### 记录跑步
```
输入：今天跑了5公里，感觉还不错
输出：
运动记录已保存！
运动类型：跑步
运动时长：30分钟
燃烧热量：300.0千卡

本月累计运动：30分钟
本月消耗热量相当于：120克瘦牛肉

太棒了！你今天完成了5公里的跑步，状态还这么好！坚持跑步不仅能增强心肺功能，还能让你保持满满的活力。继续保持，你离健康越来越近了！
```

### 记录游泳
```
输入：今天游泳了40分钟，感觉轻松
输出：
运动记录已保存！
运动类型：游泳
运动时长：40分钟
燃烧热量：500.0千卡

本月累计运动：70分钟
本月消耗热量相当于：320克瘦牛肉

太棒了！你今天游了40分钟，状态还这么轻松，真的超厉害！游泳既能锻炼全身肌肉，还能舒缓压力，坚持下去，健康和好状态都会牢牢属于你哦！
```

## 🔧 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `FEISHU_APP_TOKEN` | ✅ | 飞书多维表格的 app_token |
| `FEISHU_EXERCISE_TABLE_ID` | ✅ | 飞书多维表格的 table_id |
| `COZE_WORKSPACE_PATH` | ✅ | 项目路径（默认：/workspace/projects） |

## 💰 成本

- **Vercel**: 个人版完全免费，包含：
  - 100GB 带宽/月
  - 无限部署
  - 全球 CDN 加速
- **飞书多维表格**: 个人版免费
- **总计**: $0/月

## 📝 开发说明

### 技术栈
- **LangGraph**: 工作流编排
- **飞书多维表格**: 数据存储
- **豆包大模型**: AI 分析
- **Vercel**: 云端部署

### 添加新功能
1. 在 `src/graphs/state.py` 中添加新的状态字段
2. 在 `src/graphs/nodes/` 中创建新的节点
3. 在 `src/graphs/graph.py` 中添加节点到工作流

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
