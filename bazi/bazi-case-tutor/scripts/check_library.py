from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "references" / "library" / "case-index.md"
CASES = ROOT / "references" / "library" / "cases"
REQUIRED = [
    "## 状态与隐私",
    "## 排盘",
    "## 留出信息",
    "## 评分与错误",
    "## 可复验假设",
    "## 教学价值",
]
SENSITIVE = [r"身份证", r"手机号", r"微信号", r"精确住址", r"真实姓名"]


def main() -> int:
    errors = []
    index_text = INDEX.read_text(encoding="utf-8")
    files = sorted(CASES.glob("CASE-*.md"))
    seen = set()
    for path in files:
        match = re.fullmatch(r"CASE-(\d{3})\.md", path.name)
        if not match:
            errors.append(f"invalid case filename: {path.name}")
            continue
        case_id = path.stem
        if case_id in seen:
            errors.append(f"duplicate case id: {case_id}")
        seen.add(case_id)
        text = path.read_text(encoding="utf-8")
        for heading in REQUIRED:
            if heading not in text:
                errors.append(f"{case_id} missing {heading}")
        if case_id not in index_text:
            errors.append(f"{case_id} missing from index")
        for pattern in SENSITIVE:
            if re.search(pattern, text):
                errors.append(f"{case_id} contains sensitive-field marker: {pattern}")
    indexed = set(re.findall(r"CASE-\d{3}", index_text))
    for case_id in sorted(indexed - seen):
        errors.append(f"index references missing case: {case_id}")
    if errors:
        print("FAIL")
        print("\n".join(f"- {item}" for item in errors))
        return 1
    print(f"OK: {len(files)} case(s), index and required sections valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
