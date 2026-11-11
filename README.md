# Лабораторная работа №5

Куликов Максим, группа 202М.

[![CI](https://github.com/Merhaba228/applied-ai-lab5/actions/workflows/ci.yml/badge.svg)](https://github.com/Merhaba228/applied-ai-lab5/actions/workflows/ci.yml)

## Что проверяет GitHub Actions

Взяли очистку из ЛР3 и перенесли проверки Great Expectations из ЛР2 в Python-скрипт. При пуше и открытии или обновлении pull request GitHub запускает три проверки:

1. **Ruff** проверяет Python-код, например ищет неиспользуемые импорты и ошибки в именах.
2. **pytest** проверяет очистку на маленьких таблицах: пропуски заполняются, неправильные строки удаляются, а поездки дольше часа остаются, если укладываются в сутки.
3. **Great Expectations** проверяет весь датасет NYC Taxi до и после очистки. У сырых данных нарушения ожидаемы и выводятся в журнал. Если после очистки осталось хотя бы одно нарушение, проверка падает.

Сценарий лежит в [ci.yml](.github/workflows/ci.yml). Результаты каждого запуска видны во вкладке [Actions](https://github.com/Merhaba228/applied-ai-lab5/actions).

## Результат

Ruff не нашёл ошибок, все 12 юнит-тестов прошли. Great Expectations нашёл в сырых данных нарушения в числе пассажиров, координатах и длительности поездки. После удаления 107 строк осталось 1 458 537 поездок, и таблица прошла все проверки.

| Данные | Строк | Пройдено проверок |
| --- | ---: | ---: |
| До очистки | 1 458 644 | 15 из 21 |
| После очистки | 1 458 537 | 21 из 21 |

К правилам ЛР2 добавили одну простую проверку: таблица после очистки не должна быть пустой.

## Как повторить

Понадобятся Python 3.12, Git и Git LFS. Скачайте репозиторий и архив с данными:

```bash
git lfs install
git clone https://github.com/Merhaba228/applied-ai-lab5.git
cd applied-ai-lab5
git lfs pull
python -m venv .venv
```

Команды для Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m src.validate_data
```

На Linux и macOS вместо `.\.venv\Scripts\python.exe` используйте `.venv/bin/python`.

## Вывод

Теперь после пуша видно, не сломалась ли очистка и проходят ли обработанные данные правила ЛР2. Запускать ноутбук и проверять таблицу вручную для этого больше не нужно.
