#!/usr/bin/env python3

from devicetest.core.test_case import TestCase, Step


class testListDataDir(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        super().__init__(self.TAG, controllers)

    def setup(self):
        Step("Setup")

    def process(self):
        Step("Process")
        output = self.device1.execute_shell_command("ls /data")
        self.log.info("ls /data output: " + output)
        
        # 将输出切分成列表
        dir_list = output.split()
        
        # 升级点 1: 验证核心子系统的数据目录是否存在
        # 如果这些目录丢了，系统肯定起不来，这叫“关键路径检查”
        critical_dirs = ["app", "log", "samgr", "service", "vendor"]
        
        missing_dirs = []
        for target in critical_dirs:
            if target in dir_list:
                print(f"[CHECK] √ 核心目录 '{target}' 存在。")
            else:
                print(f"[CHECK] X 核心目录 '{target}' 丢失！")
                missing_dirs.append(target)
        
        # 如果有核心目录丢失，才报错
        if len(missing_dirs) > 0:
            print(f"[ERROR] 缺少以下关键目录: {missing_dirs}")
            assert False
        else:
            print("[SUCCESS] 文件系统结构完整性校验通过。")

    def teardown(self):
        Step("Teardown")


if __name__ == "__main__":
    case = testListDataDir(controllers=None)
    case.setup()
    case.process()
    case.teardown()
