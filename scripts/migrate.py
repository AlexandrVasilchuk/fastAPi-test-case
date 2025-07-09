#!/usr/bin/env python3
"""
Скрипт для управления миграциями базы данных
"""

import subprocess
import sys
from pathlib import Path

# Добавляем корневую папку проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_alembic_command(command: str) -> int:
    """Выполнить команду alembic"""
    try:
        result = subprocess.run(
            ["alembic"] + command.split(),
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {e}")
        print(f"stderr: {e.stderr}")
        return e.returncode


def main():
    """Основная функция"""
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python scripts/migrate.py upgrade [revision]  # Применить миграции")
        print("  python scripts/migrate.py downgrade [revision]  # Откатить миграции")
        print("  python scripts/migrate.py current  # Текущая версия")
        print("  python scripts/migrate.py history  # История миграций")
        print(
            "  python scripts/migrate.py revision --autogenerate -m 'message'  # Создать миграцию"
        )
        return 1

    command = " ".join(sys.argv[1:])
    return run_alembic_command(command)


if __name__ == "__main__":
    sys.exit(main())
