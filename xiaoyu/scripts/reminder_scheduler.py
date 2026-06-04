#!/usr/bin/env python3
"""
小雨提醒调度脚本 — 单次检查模式

用法：
    python reminder_scheduler.py          # 检查并输出到期提醒
    python reminder_scheduler.py --watch  # 轮询模式（每30秒检查一次）

单次模式适合配合 cron / Open Claw 定时任务使用。
轮询模式适合本地测试或长期运行的进程。
"""

import json
import os
import sys
import time
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
REMINDERS_FILE = os.path.join(DATA_DIR, "reminders.json")


def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        print(f"[错误] 找不到 {REMINDERS_FILE}")
        return []
    with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("reminders", [])


def save_reminders(reminders):
    data = {"version": 1, "reminders": reminders}
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(REMINDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def check_reminders():
    reminders = load_reminders()
    now = datetime.now().astimezone()
    triggered = []

    for r in reminders:
        if r.get("status") != "pending":
            continue
        trigger_at = datetime.fromisoformat(r["trigger_at"])
        if now >= trigger_at:
            r["status"] = "triggered"
            triggered.append(r)

    if triggered:
        save_reminders(reminders)

    return triggered


def main():
    if "--watch" in sys.argv:
        print("[小雨] 提醒轮询已启动，每 30 秒检查一次。按 Ctrl+C 退出。")
        try:
            while True:
                triggered = check_reminders()
                for r in triggered:
                    print(f"[提醒] {r['content']}")
                time.sleep(30)
        except KeyboardInterrupt:
            print("\n[小雨] 提醒轮询已停止。")
    else:
        triggered = check_reminders()
        if triggered:
            for r in triggered:
                print(f"[提醒] {r['content']}")
        # 单次模式：始终返回 0，让 cron 不报警


if __name__ == "__main__":
    main()
