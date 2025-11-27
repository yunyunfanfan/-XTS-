#!/usr/bin/env python3

import json

from devicetest.core.test_case import TestCase, Step


class testInitCfgJsonSyntax(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        super().__init__(self.TAG, controllers)

    def setup(self):
        Step("Setup")

    def process(self):
        Step("Process")
        cfg_dir_list = self.device1.execute_shell_command("ls /system/etc/init").strip().split()
        assert len(cfg_dir_list) > 0

        for cfg_name in cfg_dir_list:
            if not cfg_name.endswith(".cfg"):
                continue
            cfg_path = f"/system/etc/init/{cfg_name}"
            content = self.device1.execute_shell_command(f"cat {cfg_path}").strip()
            assert content != ""
            try:
                json.loads(content)
            except Exception:
                assert False

    def teardown(self):
        Step("Teardown")


if __name__ == "__main__":
    case = testInitCfgJsonSyntax(controllers=None)
    case.setup()
    case.process()
    case.teardown()
