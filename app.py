from flask import Flask, url_for, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
db= SQLAlchemy(app)
app.app_context().push()
login_manager = LoginManager(app)

@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(84), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True, index=True)
    senha = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name

class Task(db.Model):
    __tablename__ = "Tarefas"
    id_tarefa = db.Column(db.Integer, primary_key=True)
    titulo_tarefa = db.Column(db.String(84), nullable=False)
    hora_tarefa = db.Column(db.String(84), nullable=False)
    prazo_tarefa=db.Column(db.String(84), nullable=False)
    prioridade = db.Column(db.String(84), nullable=False)

    
    def __str__(self):
        return self.titulo_tarefa

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']

        user = User.query.filter_by(nome=nome).first()

        if not user:
            flash('Credenciais Incorretas')
            return redirect(url_for('login'))

        if not check_password_hash(user.senha, senha):
            flash('Credenciais Incorretas')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('users'))


    return render_template('login.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == "POST":
        user = User()
        user.email = request.form['email']
        user.nome = request.form['usuario']
        user.senha = request.form['senha']
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('cadastro.html')


@app.route("/tarefas", methods=['GET', 'POST'])
# @login_required
def tarefas():
    if request.method == "POST":
        tarefa = Task()
        tarefa.titulo_tarefa = request.form['Tarefa']
        tarefa.hora_tarefa = (date.today()).strftime("%d/%m/%Y")
        tarefa.prazo_tarefa = request.form['Prazo']
        tarefa.prioridade = request.form['Prioridade']
        db.session.add(tarefa)
        db.session.commit()
        return redirect(url_for('tarefas'))
    tarefas = Task.query.all()
    return render_template("lista.html", tasks=tarefas) 

@app.route('/deletar/<int:id>')
def deletar_tarefa(id):
    tarefa = Task.query.filter_by(id_tarefa=id).first()
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for('tarefas'))



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)