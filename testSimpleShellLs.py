#!/usr/bin/env python3

from devicetest.core.test_case import TestCase, Step


class testSimpleShellLs(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        super().__init__(self.TAG, controllers)

    def setup(self):
        Step("Setup")

    def process(self):
        Step("Process")
        output = self.device1.execute_shell_command("ls /")
        self.log.info("Rootfs dirs: " + output)
        
        # 将输出转换为列表
        dirs = output.split()
        
        # 定义 OpenHarmony 必须具备的核心分区
        # 如果少了 system 或 vendor，说明系统是不完整的
        critical_partitions = ["system", "vendor", "etc", "bin", "proc"]
        
        missing = []
        for part in critical_partitions:
            if part in dirs:
                print(f">>> [CHECK] √ 核心分区 '{part}' 存在。")
            else:
                print(f">>> [CHECK] X 核心分区 '{part}' 丢失！")
                missing.append(part)
        
        if missing:
            print(f">>> [FAILURE] 系统根目录结构不完整，缺少: {missing}")
            assert False
        else:
            print(">>> [SUCCESS] 根文件系统挂载完整，符合 OpenHarmony 标准架构。")

    def teardown(self):
        Step("Teardown")


if __name__ == "__main__":
    # Local debug entry using the stub devicetest implementation.
    case = testSimpleShellLs(controllers=None)
    case.setup()
    case.process()
    case.teardown()
