from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


# Configurações inicias


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Cliente


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    adress = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

# Página inicial que lista os clientes


@app.route('/')
def index():
    clients = Client.query.all()  # Busca todos os clientes no banco de dados
    return render_template('index.html', clients=clients)

# Página para adicionar um novo cliente


@app.route('/add', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        if (not request.form['name'] or
            not request.form['email'] or
            not request.form['phone'] or
                not request.form['adress']):
            return 'Por favor, preencha todos os campos', 400        
        new_client = Client(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            adress=request.form['adress']
        )
        db.session.add(new_client)
        db.session.commit()  # Confirma a adição do novo cliente
        return redirect(url_for('index'))
    return render_template('add_client.html')

# Página para editar um cliente


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    client = Client.query.get_or_404(id)  # Busca o cliente pelo ID
    if request.method == 'POST':
        if (not request.form['name'] or
            not request.form['email'] or
            not request.form['phone'] or
                not request.form['adress']):
            return "Todos os campos são obrigatórios", 400 
        client.name = request.form['name']
        client.email = request.form['email']
        client.phone = request.form['phone']
        client.adress = request.form['adress']
        db.session.commit()  # Confirma a edição do cliente
        return redirect(url_for('index'))
    return render_template('edit_client.html', client=client)

# Página para deletar um cliente


@app.route('/delete/<int:id>', methods=['POST'])
def delete_client(id):
    client = Client.query.get_or_404(id)  # Busca o cliente pelo ID
    db.session.delete(client)  # Deleta o cliente
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
