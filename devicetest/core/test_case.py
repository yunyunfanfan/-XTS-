import typing as _t
import subprocess
import os

class _Logger:
    def info(self, message: str) -> None:
        print(f"[INFO] {message}")

    def warning(self, message: str) -> None:
        print(f"[WARN] {message}")

    def error(self, message: str) -> None:
        print(f"[ERROR] {message}")

class _RealDevice:
    """
    修改版：不再是 Dummy，而是真正调用 HDC 的实战设备类。
    """
    def __init__(self, name: str = "device1") -> None:
        self.name = name
        self.device_sn = self._get_device_sn()

    def _get_device_sn(self) -> str:
        """尝试自动获取设备SN号"""
        try:
            res = subprocess.run("hdc list targets", shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            sn = res.stdout.strip()
            if sn and "Empty" not in sn:
                return sn
        except:
            pass
        return "Unknown_Device"

    def execute_shell_command(self, command: str) -> str:
        """
        这里被修改了！现在它会真的通过 HDC 发送命令。
        """
        print(f"[DEVICE:{self.name}] 正在执行真实命令: {command}")
        
        # 组装 HDC 命令
        # 注意：如果 command 里有特殊符号，可能需要更复杂的转义，这里处理最基础的情况
        full_cmd = f"hdc shell \"{command}\""
        
        try:
            # 调用系统的 HDC
            result = subprocess.run(
                full_cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                encoding='utf-8', 
                errors='ignore' # 防止编码错误导致脚本崩溃
            )
            
            output = result.stdout.strip()
            # 如果有错误输出，也打印一下方便调试
            if result.stderr.strip():
                print(f"[DEVICE ERROR] {result.stderr.strip()}")
                
            return output
            
        except Exception as e:
            print(f"[SYSTEM ERROR] 执行出错: {e}")
            return ""

class TestCase:
    def __init__(self, tag: str, controllers: _t.Any) -> None:
        self.TAG = tag
        self.controllers = controllers
        self.log = _Logger()
        # 修改点：实例化修改后的真设备类
        self.device1 = _RealDevice()

    def setup(self) -> None:  # type: ignore[override]
        """Override in subclasses if needed."""
        return None

    def process(self) -> None:  # type: ignore[override]
        """Override in subclasses with actual test logic."""
        return None

    def teardown(self) -> None:  # type: ignore[override]
        """Override in subclasses if needed."""
        return None

class Step:
    def __init__(self, name: str) -> None:
        print(f"[STEP] {name}")