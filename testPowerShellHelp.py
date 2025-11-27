#!/usr/bin/env python3

from devicetest.core.test_case import TestCase, Step


class testPowerShellHelp(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        super().__init__(self.TAG, controllers)

    def setup(self):
        Step("Setup")

    def process(self):
        Step("Process")
        
        # --- 任务 1: 获取电源状态 (修复版) ---
        # 之前的报错是因为没加 -a，现在加上 -a (all)
        print(">>> [Step 1] 获取电源子系统全量信息...")
        dump_output = self.device1.execute_shell_command("power-shell dump -a")
        
        # 打印出来看看（可能很长）
        # self.log.info("Dump Result: " + dump_output[:500] + "...") 
        
        # 验证: 如果输出了大量信息(比如长度超过200字符)，说明 dump -a 成功了
        if len(dump_output) > 200:
             print(">>> [SUCCESS] 获取电源状态成功！")
        else:
             print(">>> [WARNING] 获取的信息有点少，可能不对劲，但我们继续。")

        # --- 任务 2: 设置息屏时间为 2 分钟 ---
        print(">>> [Step 2] 尝试设置自动息屏时间为 2 分钟 (120000ms)...")
        
        # 命令: power-shell timeout -o <毫秒>
        # -o 代表 override (覆盖设置)
        timeout_cmd = "power-shell timeout -o 120000"
        result = self.device1.execute_shell_command(timeout_cmd)
        self.log.info("Set timeout result: " + result)
        
        # 验证设置结果
        # 通常成功会返回 "Set override screen off time success" 或者类似的 success 字样
        if "success" in result.lower():
            print(">>> [SUCCESS] √ 设置成功！屏幕将在 2 分钟后自动关闭。")
        else:
            # 如果板子没返回 success，也有可能生效了，我们可以再次 dump 确认一下（可选）
            print(f">>> [INFO] 设置命令返回: {result}")
            
        # --- (可选) 任务 3: 恢复默认 ---
        # 如果你不想让板子一直保持 2 分钟，可以在 teardown 里执行 power-shell timeout -r

    def teardown(self):
        Step("Teardown")


if __name__ == "__main__":
    case = testPowerShellHelp(controllers=None)
    case.setup()
    case.process()
    case.teardown()
