# 小雨实现指引

## 概述

本文档说明如何在 Open Claw 等 AI Agent 框架中落地小雨的各项功能。

## 数据持久化

### 存储方案

使用 JSON 文件存储在 skill 目录的 data/ 子目录下。

### 文件结构

```
xiaoyu/
├── data/
│   ├── records.json      # 用户数据记录（体重、睡眠、消费、心情、自定义）
│   ├── memory.json       # 长期记忆（用户偏好、历史事件）
│   ├── reminders.json    # 待触发提醒队列
│   └── session.json      # 当前会话状态（应对上下文压缩）
```

### records.json 数据结构

```json
{
  "version": 1,
  "records": [
    {
      "id": "rec_001",
      "type": "weight",
      "value": 63.5,
      "unit": "kg",
      "date": "2026-06-04",
      "note": "",
      "created_at": "2026-06-04T10:30:00+08:00"
    },
    {
      "id": "rec_002",
      "type": "sleep",
      "value": 6,
      "unit": "hours",
      "date": "2026-06-03",
      "note": "",
      "created_at": "2026-06-04T08:15:00+08:00"
    },
    {
      "id": "rec_003",
      "type": "expense",
      "value": 399,
      "unit": "CNY",
      "category": "购物",
      "date": "2026-06-04",
      "note": "",
      "created_at": "2026-06-04T14:20:00+08:00"
    },
    {
      "id": "rec_004",
      "type": "mood",
      "value": "一般",
      "unit": "",
      "date": "2026-06-04",
      "note": "",
      "created_at": "2026-06-04T22:00:00+08:00"
    },
    {
      "id": "rec_005",
      "type": "custom",
      "value": "健身45分钟",
      "unit": "",
      "date": "2026-06-04",
      "note": "",
      "created_at": "2026-06-04T18:00:00+08:00"
    }
  ]
}
```

字段说明：
- id: 唯一标识，格式 `rec_` + 序号
- type: 记录类型，枚举值 weight / sleep / expense / mood / custom
- value: 记录值，数值类型时存数字，文本类型时存字符串
- unit: 单位，体重默认为 kg，睡眠默认为 hours，消费默认为 CNY，心情和自定义留空
- date: 记录日期，格式 YYYY-MM-DD
- category: 仅消费类型使用，如 "餐饮" "购物" "交通"
- note: 备注
- created_at: 记录创建时间，ISO 8601 格式

### memory.json 数据结构

```json
{
  "version": 1,
  "preferences": [
    {"key": "hobby", "value": "Minecraft", "source": "explicit", "updated_at": "2026-06-01T12:00:00+08:00"},
    {"key": "device", "value": "Mac mini", "source": "inferred", "updated_at": "2026-06-01T12:00:00+08:00"},
    {"key": "interest", "value": "技术", "source": "explicit", "updated_at": "2026-06-01T12:00:00+08:00"}
  ],
  "events": [
    {"summary": "最近在减肥", "status": "active", "created_at": "2026-05-20T09:00:00+08:00"},
    {"summary": "最近研究服务器", "status": "active", "created_at": "2026-06-01T15:00:00+08:00"}
  ],
  "history": [
    {"summary": "之前在增重", "status": "resolved", "created_at": "2026-04-01T10:00:00+08:00", "resolved_at": "2026-05-20T09:00:00+08:00"}
  ]
}
```

字段说明：
- preferences: 用户长期偏好，key-value 存储，updated_at 用于判断新旧
- events: 当前活跃的历史事件，status 为 `active`
- history: 已过时或被更新的旧事件，status 为 `resolved`，保留用于追溯

### reminders.json 数据结构

```json
{
  "version": 1,
  "reminders": [
    {
      "id": "rem_001",
      "content": "开会",
      "trigger_at": "2026-06-04T13:30:00+08:00",
      "status": "pending",
      "created_at": "2026-06-04T10:00:00+08:00"
    }
  ]
}
```

字段说明：
- id: 唯一标识，格式 `rem_` + 序号
- content: 提醒内容（自然语言文本）
- trigger_at: 触发时间，ISO 8601 格式
- status: pending / triggered / cancelled

### session.json 数据结构

用于应对上下文压缩，记录当前会话状态。详见 memory.md 的"上下文压缩应对"一节。

```json
{
  "current_topic": "...",
  "pending": ["..."],
  "recent_summary": "...",
  "last_updated": "2026-06-04T15:30:00+08:00"
}
```

## 提醒调度

### 实现方式

提醒功能依赖外部调度，小雨只负责解析和存储，不负责时钟。

**推荐方案（Open Claw 环境）**：
1. 小雨解析用户消息，提取时间+内容
2. 写入 data/reminders.json，状态为 pending
3. Open Claw 框架的定时任务模块轮询 reminders.json，发现到期提醒
4. 调用小雨推送提醒消息给用户

**备选方案**：
- 使用系统 cron 或 at 命令注册定时任务
- 使用 Python schedule 库做内存轮询

### 提醒推送格式

推送时以小雨的口吻发送（参考 reminders.md），不要用系统通知格式。

## 功能依赖矩阵

| 功能 | 依赖外部调度 | 需要持久化 | 复杂度 |
|------|:----------:|:--------:|:----:|
| 聊天 | 否 | 否 | 低 |
| 情绪陪伴 | 否 | 否 | 低 |
| 知识问答 | 否 | 否 | 低 |
| 长期记忆 | 否 | 是 | 中 |
| 数据记录 | 否 | 是 | 中 |
| 数据查询 | 否 | 是 | 中 |
| 提醒 | **是** | 是 | 高 |

## 初始化检查清单

首次使用小雨时，确保以下就绪：

- [ ] data/ 目录已创建
- [ ] data/records.json 已初始化（含 `{"version": 1, "records": []}`）
- [ ] data/memory.json 已初始化（含空 preferences/events/history）
- [ ] data/reminders.json 已初始化（含 `{"version": 1, "reminders": []}`）
- [ ] data/session.json 已初始化（含空 current_topic/pending/recent_summary）
- [ ] 提醒调度机制已配置（如使用 Open Claw 的定时任务模块）

## 错误处理

- JSON 文件损坏：尝试修复，失败则重建空文件并告知用户数据可能丢失
- 日期解析失败：向用户确认日期意图，不要猜测
- 提醒时间已过：告知用户并询问是否要设置为明天同一时间
