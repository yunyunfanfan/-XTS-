#!/usr/bin/env python3

from devicetest.core.test_case import TestCase, Step


class testPrintWorkingDirectory(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        super().__init__(self.TAG, controllers)

    def setup(self):
        Step("Setup")

    def process(self):
        Step("Process")
        
        # 定义一个测试文件名
        test_file = "/data/local/tmp/xts_test_file.txt"
        
        print(f">>> [Step 1] 尝试创建文件: {test_file}")
        # touch 命令用来创建一个空文件
        self.device1.execute_shell_command(f"touch {test_file}")
        
        print(f">>> [Step 2] 验证文件是否存在")
        # ls 命令查看该文件
        check_output = self.device1.execute_shell_command(f"ls {test_file}")
        
        if "No such file" in check_output:
            print(">>> [FAILURE] 文件创建失败！可能没有写权限。")
            assert False
        else:
            print(f">>> [SUCCESS] 文件创建成功: {check_output}")

        print(f">>> [Step 3] 清理现场 (删除文件)")
        self.device1.execute_shell_command(f"rm {test_file}")
        
        # 再次确认删掉了没
        check_again = self.device1.execute_shell_command(f"ls {test_file}")
        if "No such file" in check_again:
             print(">>> [SUCCESS] 文件已成功删除。")
        else:
             print(">>> [WARNING] 文件好像没删掉？")

    def teardown(self):
        Step("Teardown")


if __name__ == "__main__":
    case = testPrintWorkingDirectory(controllers=None)
    case.setup()
    case.process()
    case.teardown()
