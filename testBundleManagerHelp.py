#!/usr/bin/env python3

from devicetest.core.test_case import TestCase, Step


class testBundleManagerHelp(TestCase):
    def __init__(self, controllers):
        self.TAG = self.__class__.__name__
        super().__init__(self.TAG, controllers)

    def setup(self):
        Step("Setup")

    def process(self):
        Step("Process")
        output = self.device1.execute_shell_command("bm help")
        self.log.info("bm help output: " + output)
        assert output != ""

    def teardown(self):
        Step("Teardown")


if __name__ == "__main__":
    case = testBundleManagerHelp(controllers=None)
    case.setup()
    case.process()
    case.teardown()
