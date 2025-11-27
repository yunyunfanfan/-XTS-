#!/usr/bin/env python3

from devicetest.core.test_case import TestCase, Step


class testShowCurrentUser(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        super().__init__(self.TAG, controllers)

    def setup(self):
        Step("Setup")

    def process(self):
        Step("Process")
        
        # --- 升级点 1: 使用 id 命令获取详细身份信息 ---
        # 输出通常长这样: uid=0(root) gid=0(root) groups=0(root),...
        output = self.device1.execute_shell_command("id")
        self.log.info("id command output: " + output)
        
        # --- 升级点 2: 验证权限 ---
        # 检查 uid 是否为 0 (0 代表 root 权限)
        if "uid=0(root)" in output:
            print(">>> [SUCCESS] 权限检查通过：当前为 Root 超级管理员权限。")
        elif "uid=2000(shell)" in output:
            print(">>> [WARNING] 当前为 Shell 普通用户权限 (受限)。")
        else:
            print(f">>> [INFO] 当前用户身份未知: {output}")
            
        # 基础断言
        assert "uid=" in output

    def teardown(self):
        Step("Teardown")


if __name__ == "__main__":
    case = testShowCurrentUser(controllers=None)
    case.setup()
    case.process()
    case.teardown()
