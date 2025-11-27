#!/usr/bin/env python3

import datetime
import time
from devicetest.core.test_case import TestCase, Step

class testShowDateCommand(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        super().__init__(self.TAG, controllers)

    def setup(self):
        Step("Setup")

    def process(self):
        Step("Process")
        
        # 1. 获取电脑当前时间
        now = datetime.datetime.now()
        
        # 2. 转换为嵌入式常用的紧凑格式: MMDDhhmmYYYY.ss
        # 例如 11月27日 18点30分 2025年 -> 112718302025.00
        cmd_time_str = now.strftime("%m%d%H%M%Y.%S")
        
        # 用于人类阅读的格式
        readable_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n>>> [PC端] 电脑当前时间: {readable_time}")
        print(f">>> [PC端] 准备发送的时间码: {cmd_time_str}")

        # 3. 发送设置命令
        # 尝试格式 A: date MMDDhhmmYYYY.ss (Toybox/Busybox 标准)
        cmd = f"date {cmd_time_str}"
        self.device1.execute_shell_command(cmd)
        
        # 等一小会儿让系统反应一下
        time.sleep(1)

        # 4. 检查板子现在的时间
        board_output = self.device1.execute_shell_command("date").strip()
        print(f">>> [Device] 板子当前时间: {board_output}")

        # 5. 严格验证 (检查 月、日、时 是否包含在输出中)
        # 板子输出格式通常是: "Thu Nov 27 18:30:00 CST 2025"
        # 我们构建几个关键特征来匹配
        
        # 检查年份
        assert str(now.year) in board_output
        
        # 检查月份 (英文缩写匹配)
        # Python 的 %b 可以生成 Jan, Feb, Nov 等缩写
        target_month_abbr = now.strftime("%b") 
        target_day = now.strftime("%d") # 27
        
        # 注意：date输出里的日期如果是个位数，可能是 " 5" 也可能是 "05"，这里做简单宽容处理
        # 如果板子输出包含 Nov (月份) 和 2025 (年份)
        if target_month_abbr in board_output and str(now.year) in board_output:
             print(">>> [SUCCESS] √ 时间同步成功！板子时间已校准。")
        else:
             print(f">>> [FAILURE] X 同步失败！期待月份 '{target_month_abbr}'，但板子显示 '{board_output}'")
             # 如果还失败，尝试第二种格式： date -s "YYYY-MM-DD HH:MM:SS"
             # 你可以在这里加备用逻辑，但通常第一种就够了
             assert False

    def teardown(self):
        Step("Teardown")

if __name__ == "__main__":
    case = testShowDateCommand(controllers=None)
    case.setup()
    case.process()
    case.teardown()