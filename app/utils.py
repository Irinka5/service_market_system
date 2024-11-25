from werkzeug.security import generate_password_hash, check_password_hash

# Функции для работы с паролями

def hash_password(password):
    """
    Генерация хеша пароля с использованием bcrypt.
    """
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

def check_password(hashed_password, password):
    """
    Проверка пароля по хешу.
    """
    return check_password_hash(hashed_password, password)

# Вспомогательные функции для других задач

def flash_errors(form):
    """
    Функция для флеш-сообщений всех ошибок в форме.
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Ошибка в поле {getattr(form, field).label.text}: {error}", 'danger')