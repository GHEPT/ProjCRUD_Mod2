from flask import (Flask, Blueprint, render_template, request)
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
bp = Blueprint('app', __name__)

# Banco de dados (Database)

user='kjysjhbu'
password='geMArjTnjJ0_CW57GMqdcOiRmUIRZE0J'
host='tuffi.db.elephantsql.com'
database='kjysjhbu'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secreta'

db = SQLAlchemy(app)

# Modelo
class Memes(db.Model):
  # db.Integer = int / serial
  id = db.Column(db.Integer, primary_key = True)
  # db.String = varchar --- nullable = not null
  modulo = db.Column(db.String(50), nullable = False)
  aula = db.Column(db.String(8), nullable = False)
  conteudo = db.Column(db.String(50), nullable = False)
  texto = db.Column(db.String(100), nullable = False)
  url1 = db.Column(db.String(350), nullable = False)
  url2 = db.Column(db.String(350), nullable = True)
  senha = db.Column(db.String(36), default=uuid.uuid4, nullable = False)

  # self = a própria tabela / a própria classe Filmes do python
  # aqui estamos declarando que um novo filme deve obedecer as especificações declaradas acima
  def __init__(self, modulo, aula, conteudo, texto, url1, url2):
    self.modulo = modulo
    self.aula = aula
    self.conteudo = conteudo
    self.texto = texto
    self.url1 = url1
    self.url2 = url2
    
  @staticmethod
  def read_single():
    # SELECT * from filmes order by id asc;
    return Memes.query.order_by(Memes.id.desc()).all()
    # SELECT * from filmes;
    #return Filmes.query.all()

  @staticmethod
  def read_all(meme_id): #Troquei meu read_single pelo read_all só nome
    # SELECT * from filmes where id = <id_de_um_filme>;
    return Memes.query.get(meme_id)
  
  def save(self): 
    db.session.add(self) # estamos adicionando as informações passadas no form (modulo, aula, conteudo, texto e url) para o Banco de Dados (utilizando sessão)
    db.session.commit()

  def update(self, new_data):
    self.modulo = new_data.modulo
    self.aula = new_data.aula
    self.conteudo = new_data.conteudo
    self.texto = new_data.texto
    self.url1 = new_data.url1
    self.url2 = new_data.url2
    self.save()
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  

@bp.route('/')
def home():
  return render_template('index.html')

@bp.route('/read')
def read_single():
  meme = Memes.read_single()
  return render_template('read_single.html', memes=meme) # Passando para dentro do nosso HTML os dados da minha listagem de filmes!!!!

@bp.route('/read/<meme_id>')
def lista_detalhe_meme(meme_id):
  meme = Memes.read_all(meme_id)
  return render_template('read_all.html', meme=meme)

@bp.route('/create', methods=('GET', 'POST'))
def create():
  id_atribuido = None
#Como o método utilizado no formulário é POST, pegamos os valores dos campos
  if request.method =='POST':
    form=request.form
    meme = Memes(form['modulo'], form['aula'], form['conteudo'], form['texto'], form['url1'], form['url2']) 
    meme.save()
    id_atribuido=meme.senha
  return render_template('create.html', id_atribuido=id_atribuido)

#Rota do Update

@bp.route('/update/<meme_id>',methods=('GET', 'POST'))
def update(meme_id):
  sucesso = None
  meme = Memes.read_all(meme_id)  

  if request.method =='POST':
    form=request.form
    new_data = Memes(form['modulo'], form['aula'], form['conteudo'], form['texto'], form['url1'], form['url2'])
    meme.update(new_data)
    sucesso = True
  return render_template('update.html', meme=meme, sucesso=sucesso)

@bp.route('/delete/<meme_id>') # Rota de confirmação de delete. confirmar perdir para o usuário(@) se ele realmente quer deletar o filme.

def delete(meme_id):
  meme = Memes.read_all(meme_id)
  return render_template('delete.html', meme=meme)


@bp.route('/delete/<meme_id>/confirmed') # rota que confirma a deleção do resgistro, e mostra a mensagem de deleção concluída.
def delete_confirmed(meme_id):
  sucesso = None
  meme = Memes.read_all(meme_id)
  if meme:
    meme.delete()
    sucesso = True
  return render_template('delete.html', sucesso=sucesso)


# Pega os dados do blueprint da nossa aplicação (nome do app e as rotas) e registra dentro do app do Flask
app.register_blueprint(bp)


if __name__ == '__main__':
  app.run(debug=True)
