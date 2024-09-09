import subprocess
import time
import os


def start_script(script_name):
    """启动指定的 Python 脚本并返回进程对象。"""
    return subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def monitor_and_restart():
    """启动 monitor.py 和 crawler.py，并处理重启逻辑。"""
    monitor_script = "monitor.py"
    crawler_script = "crawler.py"

    # 启动 monitor.py
    monitor_process = start_script(monitor_script)
    print(f"{monitor_script} 已启动。")

    # 启动 crawler.py
    crawler_process = start_script(crawler_script)
    print(f"{crawler_script} 已启动。")

    try:
        while True:
            # 检查 monitor.py 和 crawler.py 是否仍在运行
            monitor_alive = monitor_process.poll() is None
            crawler_alive = crawler_process.poll() is None

            if not monitor_alive:
                print(f"{monitor_script} 停止运行，重新启动...")
                monitor_process = start_script(monitor_script)

            if not crawler_alive:
                print(f"{crawler_script} 停止运行，重新启动...")
                crawler_process = start_script(crawler_script)

            time.sleep(10)  # 每10秒检查一次
    except KeyboardInterrupt:
        print("检测到中断信号，关闭所有进程...")
    finally:
        monitor_process.terminate()
        crawler_process.terminate()
        monitor_process.wait()
        crawler_process.wait()
        print("所有进程已关闭。")


if __name__ == "__main__":
    monitor_and_restart()
