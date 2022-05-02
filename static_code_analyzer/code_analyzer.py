import argparse
from pathlib import Path


def line_too_long(line: str) -> bool:
    return len(line) > 79


def wrong_indentation_basic(line: str) -> bool:
    return line.index(line.lstrip()) % 4 != 0


def semicolon_after_statement(line: str) -> bool:
    return line.split("#")[0].rstrip().endswith(";")


def bad_spacing_before_comment(line: str) -> bool:
    return (
        not line.startswith("#")
        and "#" in line
        and not line.split("#")[0].endswith("  ")
    )


def todo_comment_found(line: str) -> bool:
    return "#" in line and "todo" in line.split("#")[1].lower()


line_checks = {
    line_too_long: ("S001", "Line is too long"),
    wrong_indentation_basic: ("S002", "Indentation is not a multiple of four"),
    semicolon_after_statement: ("S003", "Unnecessary semicolon after a statement"),
    bad_spacing_before_comment: ("S004", "Less than two spaces before inline comment"),
    todo_comment_found: ("S005", "TODO comment found"),
}


def error_msg(path: Path, n_line: int, errcode: str, msg: str) -> str:
    return f"{path}: Line {n_line}: {errcode} {msg}"


def check_file(path: Path) -> None:
    with path.open() as file:
        prev_blank_lines = 0

        for i, line in enumerate(file, 1):
            for check, (errcode, msg) in line_checks.items():
                if check(line):
                    print(error_msg(path, i, errcode, msg))

            if line.isspace():
                prev_blank_lines += 1
            elif prev_blank_lines > 2:
                prev_blank_lines = 0
                print(error_msg(path, i, "S006", "Too many blank lines"))


def check_path(path: Path) -> None:
    if path.is_file() and path.suffix == ".py":
        check_file(path)
    elif path.is_dir():
        for p in path.rglob("*.py"):
            check_file(p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the file or directory to check")
    check_path(Path(parser.parse_args().path))