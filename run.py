from app import create_app, db

# Создание экземпляра приложения
app = create_app()

if __name__ == "__main__":
    # Запуск приложения на локальном сервере
    app.run(host="0.0.0.0", port=5000, debug=True)