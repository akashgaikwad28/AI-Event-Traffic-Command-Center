import subprocess
import sys


def run_command(command: list) -> bool:
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"FAILED: {' '.join(command)}")
        return False
    return True


def main():
    print("=== GridWise AI Quality Gate ===")

    commands = [
        ["ruff", "check", "."],
        ["black", "--check", "."],
        ["mypy", "."],
        ["pytest", "--cov=backend/app", "--cov-fail-under=85"],
    ]

    for cmd in commands:
        if not run_command(cmd):
            print("\n❌ Quality Gate Failed.")
            sys.exit(1)

    print("\n✅ Quality Gate Passed. GridWise AI is production-ready.")
    sys.exit(0)


if __name__ == "__main__":
    main()
