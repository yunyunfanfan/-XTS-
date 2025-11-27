import os
import glob
import subprocess
import time
import datetime

# --- 配置区域 ---
# 报告文件名
REPORT_FILE = "XTS_Report.html"
# 你的测试脚本通常以什么开头？
TEST_PATTERN = "test*.py"
# ----------------

def generate_html_header():
    return """
    <html>
    <head>
        <meta charset="utf-8">
        <title>OpenHarmony XTS 测试报告</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 20px; }
            h1 { color: #333; text-align: center; }
            .summary { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .pass { color: green; font-weight: bold; }
            .fail { color: red; font-weight: bold; }
            table { width: 100%; border-collapse: collapse; background: #fff; }
            th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            th { background-color: #007bff; color: white; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .log-box { display: none; background: #333; color: #0f0; padding: 10px; font-family: monospace; font-size: 12px; white-space: pre-wrap; margin-top: 5px; border-radius: 4px; }
            button { cursor: pointer; background: #eee; border: 1px solid #ccc; padding: 5px 10px; border-radius: 4px; }
        </style>
        <script>
            function toggleLog(id) {
                var x = document.getElementById(id);
                if (x.style.display === "none") {
                    x.style.display = "block";
                } else {
                    x.style.display = "none";
                }
            }
        </script>
    </head>
    <body>
        <h1>OpenHarmony XTS 自动化测试报告</h1>
    """

def run_tests():
    # 1. 找到所有测试文件
    test_files = glob.glob(TEST_PATTERN)
    # 排除掉自己，防止死循环
    if "run_all.py" in test_files:
        test_files.remove("run_all.py")
    
    # 按文件名排序
    test_files.sort()
    
    results = []
    total = len(test_files)
    passed = 0
    failed = 0
    
    print(f">>> 发现 {total} 个测试脚本，准备开始执行...\n")
    
    html_content = generate_html_header()
    table_rows = ""
    
    start_time_all = datetime.datetime.now()

    for idx, script in enumerate(test_files):
        print(f"[{idx+1}/{total}] 正在运行: {script} ...", end="", flush=True)
        
        # 运行单个脚本
        # capture_output=True 会把脚本的 print 内容抓取下来
        start_time = time.time()
        try:
            # 这里的 python 命令会根据你系统环境变量里的 python 来运行
            proc = subprocess.run(["python", script], capture_output=True, text=True, encoding='utf-8', errors='ignore')
            output_log = proc.stdout + "\n" + proc.stderr
            return_code = proc.returncode
        except Exception as e:
            output_log = f"脚本执行异常: {str(e)}"
            return_code = -1
        
        duration = time.time() - start_time
        
        # 判断结果
        status_class = "pass" if return_code == 0 else "fail"
        status_text = "PASS" if return_code == 0 else "FAIL"
        
        if return_code == 0:
            passed += 1
            print(" [PASS]")
        else:
            failed += 1
            print(" [FAIL]")
            
        # 生成表格行
        log_id = f"log_{idx}"
        row = f"""
        <tr>
            <td>{idx + 1}</td>
            <td>{script}</td>
            <td class="{status_class}">{status_text}</td>
            <td>{duration:.2f}s</td>
            <td>
                <button onclick="toggleLog('{log_id}')">查看日志</button>
                <div id="{log_id}" class="log-box">{output_log}</div>
            </td>
        </tr>
        """
        table_rows += row
        
    end_time_all = datetime.datetime.now()
    duration_all = end_time_all - start_time_all
    
    # 生成摘要部分
    success_rate = (passed / total) * 100 if total > 0 else 0
    summary_html = f"""
    <div class="summary">
        <h2>测试汇总</h2>
        <p><strong>执行时间:</strong> {start_time_all.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>耗时:</strong> {duration_all}</p>
        <p><strong>总用例数:</strong> {total}</p>
        <p><span class="pass">成功: {passed}</span> | <span class="fail">失败: {failed}</span></p>
        <p><strong>通过率:</strong> {success_rate:.2f}%</p>
    </div>
    <table>
        <thead>
            <tr>
                <th>序号</th>
                <th>脚本名称</th>
                <th>结果</th>
                <th>耗时</th>
                <th>详细日志</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    </body></html>
    """
    
    html_content += summary_html
    
    # 写入文件
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n>>> 测试结束！")
    print(f">>> 报告已生成: {os.path.abspath(REPORT_FILE)}")

if __name__ == "__main__":
    run_tests()