#!/usr/bin/env python3

from devicetest.core.test_case import TestCase, Step


class testSystemInitDirNotEmpty(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        super().__init__(self.TAG, controllers)

    def setup(self):
        Step("Setup")

    def process(self):
        Step("Process")
        output = self.device1.execute_shell_command("ls /system/etc/init")
        self.log.info("ls /system/etc/init output: " + output)
        entries = [name for name in output.strip().split() if name]
        assert len(entries) > 0

    def teardown(self):
        Step("Teardown")


if __name__ == "__main__":
    case = testSystemInitDirNotEmpty(controllers=None)
    case.setup()
    case.process()
    case.teardown()
