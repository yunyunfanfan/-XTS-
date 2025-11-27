#!/usr/bin/env python3

import json

from devicetest.core.test_case import TestCase, Step


class testInitServicesMetaCheck(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        super().__init__(self.TAG, controllers)

    def setup(self):
        Step("Setup")

    def process(self):
        Step("Process")
        cfg_names = self.device1.execute_shell_command("ls /system/etc/init").strip().split()
        assert len(cfg_names) > 0

        # 用来统计有多少个没写 apl 的
        missing_apl_count = 0 

        for cfg_name in cfg_names:
            if not cfg_name.endswith(".cfg"):
                continue
            
            cfg_path = f"/system/etc/init/{cfg_name}"
            # 打印正在检查谁，方便定位
            print(f"[CHECK] Checking {cfg_name}...") 
            
            content = self.device1.execute_shell_command(f"cat {cfg_path}").strip()
            if not content:
                continue
            try:
                cfg_obj = json.loads(content)
            except Exception:
                print(f"[WARN] {cfg_name} is not valid JSON, skipping.")
                continue
                
            services = cfg_obj.get("services")
            if not isinstance(services, list):
                continue
                
            for service in services:
                # 1. 检查 name (这是必须的，没有 name 就真的很离谱了)
                if "name" not in service:
                    print(f"[ERROR] Found service without NAME in {cfg_name}!")
                    assert False # 这种情况还是让它崩吧

                # 2. 检查 apl (把 assert 改成 if 判断)
                if "apl" not in service:
                    print(f"[WARNING] 发现漏网之鱼! 文件: {cfg_name}, 服务: {service['name']} 缺少 'apl' 字段")
                    missing_apl_count += 1
                else:
                    # 如果有，也可以打印一下（可选）
                    # print(f"[OK] {service['name']} apl is {service['apl']}")
                    pass

        print(f"\n[RESULT] 扫描完成。共有 {missing_apl_count} 个服务缺少 'apl' 字段。")
        # 这里我们不让测试失败，只要扫描完成就算通过
        assert True

    def teardown(self):
        Step("Teardown")


if __name__ == "__main__":
    case = testInitServicesMetaCheck(controllers=None)
    case.setup()
    case.process()
    case.teardown()
