# 小雨 (Xiaoyu)

一个个人长期自用的 AI 微信好友，定位为"像真人朋友，但同时具备个人助理能力"。

## 核心特性

- **自然聊天** - 像微信好友一样对话，温柔自然，轻微真人感
- **数据记录** - 记录体重、睡眠、消费、心情等个人数据
- **提醒功能** - 设置单次提醒，在指定时间推送
- **知识问答** - 回答技术问题、日常百科、学习问题
- **长期记忆** - 记住用户偏好和历史事件，保持对话连续性

## 目录结构

```
xiaoyu/
├── SKILL.md              # 主文档，包含完整功能说明
├── agents/
│   └── openai.yaml       # Open Claw agent 配置
├── data/
│   ├── records.json      # 用户数据记录
│   ├── memory.json       # 长期记忆
│   ├── reminders.json    # 提醒队列
│   └── session.json      # 会话状态
├── references/
│   ├── personality.md    # 人格与语气规则
│   ├── memory.md         # 记忆系统规则
│   ├── recording.md      # 数据记录规则
│   ├── reminders.md      # 提醒系统规则
│   └── implementation.md # 实现指引
└── scripts/
    └── reminder_scheduler.py  # 提醒调度脚本
```

## 快速开始

1. 确保 `data/` 目录下 4 个 JSON 文件已初始化
2. 如需提醒功能，启动 `scripts/reminder_scheduler.py --watch`
3. 以自然语言与小雨对话即可

## 使用示例

```
小雨，最近有点烦。
记录今天体重 63.5kg
小雨下午 13:30 有会
这个 VPN 怎么配置？
```

## 设计原则

- **用户驱动** - 只在用户触发时响应，不主动推送
- **最小侵入** - 不擅自记录信息，仅用户明确要求才写入
- **自然交互** - 无需命令格式，允许自然语言表达

详见 [SKILL.md](SKILL.md) 了解完整文档。
