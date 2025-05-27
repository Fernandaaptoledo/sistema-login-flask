
from flask import Flask, render_template, request, redirect, session, url_for
from auth import autenticar_usuario, registrar_usuario, logout_usuario, usuario_logado
from database import init_db

app = Flask(__name__)
app.secret_key = 'segredo-super-seguro'

init_db()

@app.route('/')
def home():
    if not usuario_logado():
        return redirect(url_for('login'))
    return render_template('home.html', nome=session['usuario'])

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        sucesso, mensagem = registrar_usuario(nome, email, senha)
        if sucesso:
            return redirect('/login')
        else:
            return render_template('cadastro.html', erro=mensagem)
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        sucesso, nome = autenticar_usuario(email, senha)
        if sucesso:
            session['usuario'] = nome
            return redirect('/')
        else:
            return render_template('login.html', erro='E-mail ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_usuario()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
