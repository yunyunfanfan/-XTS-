import argparse
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


def _parse_junit_results(run_dir: Path, junit_pattern: str):
    """Parse JUnit-style XML reports under run_dir matching junit_pattern.

    This is a best-effort parser: if no files match, an empty stats dict is
    returned and the caller can treat it as "no case-level data".
    """

    if not junit_pattern:
        return None

    total = 0
    passed = 0
    failed = 0
    skipped = 0
    cases = []

    for xml_file in run_dir.rglob(junit_pattern):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except Exception:
            # Ignore files that cannot be parsed as XML.
            continue

        for case in root.iter("testcase"):
            total += 1
            name = case.get("name") or ""
            classname = case.get("classname") or ""
            status = "passed"

            if case.find("failure") is not None or case.find("error") is not None:
                status = "failed"
                failed += 1
            elif case.find("skipped") is not None:
                status = "skipped"
                skipped += 1
            else:
                passed += 1

            cases.append(
                {
                    "name": name,
                    "classname": classname,
                    "status": status,
                    "file": str(xml_file),
                }
            )

    if total == 0:
        return None

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "cases": cases,
    }


def run_single_plan(xdevice_cmd, plan_path, output_dir, junit_pattern):
    plan_path = Path(plan_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plan_name = plan_path.stem
    run_id = f"{plan_name}_{timestamp}"
    run_dir = output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    stdout_file = run_dir / "xdevice_stdout.log"
    stderr_file = run_dir / "xdevice_stderr.log"

    cmd = [
        sys.executable,
        xdevice_cmd,
        "run",
        "-p",
        str(plan_path),
    ]

    start_time = datetime.now().isoformat(timespec="seconds")
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    end_time = datetime.now().isoformat(timespec="seconds")

    stdout_file.write_text(result.stdout, encoding="utf-8", errors="ignore")
    stderr_file.write_text(result.stderr, encoding="utf-8", errors="ignore")

    status = "success" if result.returncode == 0 else "failed"

    case_stats = _parse_junit_results(run_dir, junit_pattern) if junit_pattern else None

    summary = {
        "plan_name": plan_name,
        "plan_path": str(plan_path),
        "run_id": run_id,
        "run_dir": str(run_dir),
        "start_time": start_time,
        "end_time": end_time,
        "return_code": result.returncode,
        "status": status,
        "case_stats": case_stats,
    }

    return summary


def run_batch(xdevice_cmd, plans, output_dir, report_name, junit_pattern):
    batch_start = datetime.now().isoformat(timespec="seconds")
    all_results = []

    total_cases = 0
    total_passed = 0
    total_failed = 0
    total_skipped = 0

    for plan in plans:
        summary = run_single_plan(xdevice_cmd, plan, output_dir, junit_pattern)
        all_results.append(summary)

        case_stats = summary.get("case_stats") or {}
        total_cases += case_stats.get("total", 0)
        total_passed += case_stats.get("passed", 0)
        total_failed += case_stats.get("failed", 0)
        total_skipped += case_stats.get("skipped", 0)

        print(
            f"[xts-batch] {summary['plan_name']} -> {summary['status']} (code={summary['return_code']})"
        )

    batch_end = datetime.now().isoformat(timespec="seconds")

    overall = {
        "total_cases": total_cases,
        "passed": total_passed,
        "failed": total_failed,
        "skipped": total_skipped,
    }

    report = {
        "batch_start": batch_start,
        "batch_end": batch_end,
        "overall": overall,
        "plans": all_results,
    }

    output_dir = Path(output_dir).resolve()
    json_report = output_dir / f"{report_name}.json"
    md_report = output_dir / f"{report_name}.md"

    json_report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = []
    lines.append(f"# XTS 批量执行报告: {report_name}")
    lines.append("")
    lines.append(f"开始时间: {batch_start}")
    lines.append(f"结束时间: {batch_end}")
    lines.append("")

    if total_cases > 0:
        success_rate = (total_passed / total_cases) * 100.0
        lines.append("## 用例总体统计")
        lines.append("")
        lines.append(f"- 总用例数: {total_cases}")
        lines.append(f"- 通过: {total_passed}")
        lines.append(f"- 失败: {total_failed}")
        lines.append(f"- 跳过: {total_skipped}")
        lines.append(f"- 通过率: {success_rate:.2f}%")
        lines.append("")

    lines.append("## 计划级结果")
    lines.append("")
    lines.append("| 计划名 | 状态 | 返回码 | 用例数 | 通过 | 失败 | 跳过 | 结果目录 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")

    for item in all_results:
        cs = item.get("case_stats") or {}
        lines.append(
            "| {plan} | {status} | {code} | {total} | {passed} | {failed} | {skipped} | {dir} |".format(
                plan=item["plan_name"],
                status=item["status"],
                code=item["return_code"],
                total=cs.get("total", 0),
                passed=cs.get("passed", 0),
                failed=cs.get("failed", 0),
                skipped=cs.get("skipped", 0),
                dir=item["run_dir"],
            )
        )

    md_report.write_text("\n".join(lines), encoding="utf-8")

    print(f"[xts-batch] JSON 报告: {json_report}")
    print(f"[xts-batch] Markdown 报告: {md_report}")


def parse_args():
    parser = argparse.ArgumentParser(description="批量执行 XTS 计划并生成汇总报告")

    parser.add_argument(
        "--xdevice",
        dest="xdevice_cmd",
        required=True,
        help="xdevice 脚本路径，例如 /path/to/xdevice.py 或 xdevice/__main__.py",
    )

    parser.add_argument(
        "--plan",
        dest="plans",
        action="append",
        required=True,
        help="XTS JSON 配置文件路径，可重复指定多次",
    )

    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default="./xts_batch_results",
        help="批量执行结果输出目录",
    )

    parser.add_argument(
        "--report-name",
        dest="report_name",
        default="xts_batch_report",
        help="汇总报告基础文件名（不含扩展名）",
    )

    parser.add_argument(
        "--junit-pattern",
        dest="junit_pattern",
        default=None,
        help=(
            "可选：Junit XML 报告文件匹配模式，例如 'junit-*.xml'。"
            " 若不指定，则不会尝试解析用例级结果，仅按计划级返回码统计。"
        ),
    )

    return parser.parse_args()


def main():
    args = parse_args()
    run_batch(
        args.xdevice_cmd,
        args.plans,
        args.output_dir,
        args.report_name,
        args.junit_pattern,
    )


if __name__ == "__main__":
    main()
