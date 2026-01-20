# main.py
"""
Единая точка запуска:
- Поднимает Flask-бекенд (backend.app:create_app)
- Отдаёт собранный фронтенд из frontend/dist как SPA
- API доступен по /api/*
Запуск:
    python3 main.py
"""

from pathlib import Path

from flask import send_from_directory, abort
from backend.app import create_app

# Создаём приложение как обычно
app = create_app()

# Путь к собранному фронтенду
ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = ROOT_DIR / "frontend" / "dist"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path: str):
    """
    Отдаём статику фронта.
    Важные моменты:
    - /api/* НЕ трогаем (пусть обрабатывается бекендом)
    - Если файл существует в dist — отдаём его
    - Иначе отдаём index.html (SPA-роутинг: React Router, Vue Router, etc.)
    """
    # Не перехватываем API-маршруты
    if path.startswith("api/"):
        abort(404)

    # Если dist не собран — понятная ошибка
    if not FRONTEND_DIST.exists():
        return {
            "error": "Frontend is not built. Run 'npm run build' in ./frontend",
        }, 500

    # Если запрашиваемый файл существует — вернуть его
    requested = FRONTEND_DIST / path
    if path and requested.exists() and requested.is_file():
        # Например: /assets/index-XXXX.js
        rel_path = requested.relative_to(FRONTEND_DIST)
        return send_from_directory(FRONTEND_DIST, rel_path.as_posix())

    # Иначе — главный index.html (SPA)
    return send_from_directory(FRONTEND_DIST, "index.html")


if __name__ == "__main__":
    # Можно вынести хост/порт в переменные окружения при желании
    # 5000 выбран специально: совпадает с дефолтным портом Flask и прокси Vite
    app.run(host="0.0.0.0", port=8080, debug=True)