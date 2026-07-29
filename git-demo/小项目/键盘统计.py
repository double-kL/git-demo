import time
import threading
import json
import os
from collections import defaultdict
from datetime import datetime

import psutil
import win32gui
import win32process
from pynput import keyboard

# ========== 配置 ==========
HISTORY_FILE = "key_history.json"

# ========== 全局数据 ==========
key_count = 0
key_details = defaultdict(int)
window_stats = defaultdict(float)
current_hwnd = None
current_win_name = "系统桌面"
window_start_time = time.time()
last_win_name = "系统桌面"
running = True

# ========== 历史数据读写（函数同之前，精简版） ==========
def load_today_data():
    global key_count, key_details, window_stats
    today_str = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(HISTORY_FILE): return
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        today_data = data.get("daily", {}).get(today_str)
        if today_data:
            keys = today_data.get("keys", {})
            for k, v in keys.items(): key_details[k] = v
            key_count = sum(key_details.values())
            apps = today_data.get("apps", {})
            for app, seconds in apps.items(): window_stats[app] = seconds
            print(f"📂 加载今日历史：已按键 {key_count} 次")
    except Exception as e:
        print(f"⚠️ 加载失败: {e}")

def save_today_data():
    today_str = datetime.now().strftime("%Y-%m-%d")
    data = {}
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    data.setdefault("daily", {})[today_str] = {
        "keys": dict(key_details),
        "apps": {k: v for k, v in window_stats.items()}
    }
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 数据已保存")

def get_active_window_info():
    try:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd == 0: return None, "系统桌面"
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        process_name = process.name()
        title = win32gui.GetWindowText(hwnd)
        if title: return hwnd, f"{process_name} - {title[:25]}"
        else: return hwnd, f"{process_name} (无标题)"
    except: return None, "系统界面"

def update_window_time():
    global current_hwnd, current_win_name, window_start_time, last_win_name, running
    while running:
        try:
            hwnd, win_name = get_active_window_info()
            now = time.time()
            if current_hwnd is not None and current_hwnd != hwnd:
                elapsed = now - window_start_time
                if elapsed > 0.2: window_stats[last_win_name] += elapsed
            if hwnd is not None:
                current_hwnd = hwnd; current_win_name = win_name
                window_start_time = now; last_win_name = win_name
        except: pass
        time.sleep(0.5)

def on_press(key):
    global key_count
    try:
        k = key.char if hasattr(key, 'char') and key.char is not None else str(key).replace('Key.', '')
        key_details[k] += 1
        key_count += 1
    except: pass

def on_release(key):
    if key == keyboard.Key.esc:
        print("\n⚠️ 检测到 ESC 键，正在安全退出...")
        global running
        running = False
        return False

def print_final_report():
    # 结算最后窗口
    if current_hwnd is not None and window_start_time is not None:
        elapsed = time.time() - window_start_time
        if elapsed > 0.5: window_stats[last_win_name] += elapsed
    
    print("\n" + "="*60)
    print("          📊 后台静默统计报告")
    print("="*60)
    print(f"\n📅 【今日汇总】 总按键: {key_count:,}")
    print("  按键 TOP 5:")
    for i, (k, v) in enumerate(sorted(key_details.items(), key=lambda x: x[1], reverse=True)[:5], 1):
        print(f"    {i}. {k:>8} : {v:,} 次")
    print("  应用时长 TOP 5:")
    for i, (name, seconds) in enumerate(sorted(window_stats.items(), key=lambda x: x[1], reverse=True)[:5], 1):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        print(f"    {i}. {name[:35]:<35} : {minutes:>2}分{secs:>2}秒")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    load_today_data()
    threading.Thread(target=update_window_time, daemon=True).start()
    print("🚀 后台监控已启动（无界面模式）")
    print("💡 按 ESC 键 或 Ctrl+C 停止并保存数据")
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\n🛑 收到退出信号")
            running = False
    
    save_today_data()
    print_final_report()