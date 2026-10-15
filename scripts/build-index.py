#!/usr/bin/env python3
"""扫描 cases/ 下的卡片，生成 README 里的案例目录索引。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "cases"
README = ROOT / "README.md"

SECTION_NAMES = {
    "video": "🎬 视频生产",
    "archive": "🗂️ 档案与知识管理",
    "email": "📧 邮件与信息处理",
    "skills": "🛠️ 技能包",
    "messaging": "💬 消息与沟通",
}


def card_title(md: Path) -> str:
    text = md.read_text(encoding="utf-8")
    m = re.search(r"^##\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else md.stem


def main() -> None:
    lines = []
    for section in sorted(CASES.iterdir()):
        if not section.is_dir():
            continue
        name = SECTION_NAMES.get(section.name, section.name)
        lines.append(f"- {name}")
        for card in sorted(section.glob("*.md")):
            rel = card.relative_to(ROOT).as_posix()
            lines.append(f"  - [{card_title(card)}]({rel})")
        lines.append("")
    index = "\n".join(lines).rstrip()

    text = README.read_text(encoding="utf-8")
    start = "<!-- 由 scripts/build-index.py 自动生成 -->"
    new_section = f"{start}\n\n{index}\n"
    pattern = re.compile(
        re.escape(start) + r".*?(?=\n## |\Z)", re.S
    )
    if pattern.search(text):
        text = pattern.sub(lambda _: new_section, text, count=1)
    else:
        text = text.rstrip() + "\n\n" + new_section + "\n"
    README.write_text(text, encoding="utf-8")
    print(f"已更新 {README}，共 {index.count('  - [')} 个案例")


if __name__ == "__main__":
    main()
