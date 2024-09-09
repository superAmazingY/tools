import time
import subprocess
import os

def monitor_and_restart():
    start_page = 2
    total_page = 10
    word = '黄色安全服'
    per_page = 30
    delay = 0.05

    while True:
        # 检查重启触发文件是否存在
        if os.path.exists("restart_trigger.txt"):
            print("检测到重启信号，准备重启爬虫程序...")
            os.remove("restart_trigger.txt")  # 删除触发文件
            start_page += 1  # 增加起始页数
            # 重新启动爬虫程序
            subprocess.run(["python", "./crawler.py", "-w", word, "-tp", str(total_page), "-sp", str(start_page), "-pp", str(per_page), "-d", str(delay)])
        time.sleep(5)  # 每5秒检查一次

if __name__ == "__main__":
    monitor_and_restart()
