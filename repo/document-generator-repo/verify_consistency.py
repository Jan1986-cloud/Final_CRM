import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BACKEND_LOGIN_PATH = BASE_DIR / 'document-generator-backend' / 'src' / 'routes' / 'auth.py'
FRONTEND_AUTH_SERVICE = BASE_DIR / 'document-generator-frontend' / 'src' / 'services' / 'authService.js'


def find_backend_login_field():
    text = BACKEND_LOGIN_PATH.read_text()
    login_section = re.search(r"@auth_bp.route\('/login'.*?def login\(\):([^@]+)", text, re.S)
    if not login_section:
        return 'unknown'
    body = login_section.group(1)
    if "data.get('email'" in body:
        return 'email'
    if "data.get('username'" in body:
        return 'username'
    return 'unknown'


def find_frontend_login_field():
    text = FRONTEND_AUTH_SERVICE.read_text()
    m = re.search(r"post\('/auth/login',\s*{([^}]+)}\)", text)
    if not m:
        return 'unknown'
    body = m.group(1)
    if 'username' in body:
        return 'username'
    if 'email' in body:
        return 'email'
    return 'unknown'


def check_api_endpoints():
    backend_field = find_backend_login_field()
    frontend_field = find_frontend_login_field()
    if backend_field != frontend_field:
        print(f"Login field mismatch: backend expects '{backend_field}', frontend sends '{frontend_field}'")
    else:
        print('Login fields are consistent.')


if __name__ == '__main__':
    check_api_endpoints()
