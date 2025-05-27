
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

def registrar_usuario(nome, email, senha):
    db = get_db()
    try:
        senha_hash = generate_password_hash(senha)
        db.execute("INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)", (nome, email, senha_hash))
        db.commit()
        return True, "Usuário registrado com sucesso"
    except Exception as e:
        return False, "Erro: E-mail já está em uso"

def autenticar_usuario(email, senha):
    db = get_db()
    user = db.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    if user and check_password_hash(user['senha_hash'], senha):
        return True, user['nome']
    return False, None

def logout_usuario():
    from flask import session
    session.pop('usuario', None)

def usuario_logado():
    from flask import session
    return 'usuario' in session
