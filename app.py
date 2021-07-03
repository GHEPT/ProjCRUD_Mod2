from flask import (Flask, Blueprint, render_template,request)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bp = Blueprint('app', __name__)

# Banco de dados (Database)

user='rcmuzfky'
password='sSOvZIR1dVS7L4ZLM-LgQnSLBeOveOPE'
host='tuffi.db.elephantsql.com'
database='rcmuzfky'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secreta'

db = SQLAlchemy(app)

# Modelo
class Filmes(db.Model):
  # db.Integer = int / serial
  id = db.Column(db.Integer, primary_key = True)
  # db.String = varchar --- nullable = not null
  nome = db.Column(db.String(50), nullable = False)
  imagem_url = db.Column(db.String(255), nullable = False)

  # self = a própria tabela / a própria classe Filmes do python
  # aqui estamos declarando que um novo filme deve obedecer as especificações declaradas acima
  def __init__(self, nome, imagem_url):
    self.nome = nome
    self.imagem_url = imagem_url

  @staticmethod
  def read_all():
    # SELECT * from filmes order by id asc;
    return Filmes.query.order_by(Filmes.id.asc()).all()
    # SELECT * from filmes;
    #return Filmes.query.all()

  @staticmethod
  def read_single(filme_id):
    # SELECT * from filmes where id = <id_de_um_filme>;
    return Filmes.query.get(filme_id)
  
  def save(self): 
    db.session.add(self) # estamos adicionando as informações passadas no form (Nome, url) p/ o Banco de Dados (utilizando sessão)
    db.session.commit()

  def update(self, new_data):
    self.nome = new_data.nome
    self.imagem_url = new_data.imagem_url
    self.save()
  


@bp.route('/')
def home():
  return render_template('index.html')

@bp.route('/read')
def listar_filmes():
  filmes = Filmes.read_all()

  return render_template('listar-filmes.html', listaDeFilmes=filmes) # Passando para dentro do nosso HTML os dados da minha listagem de filmes!!!!

@bp.route('/read/<filme_id>')
def lista_detalhe_filme(filme_id):
  filme = Filmes.read_single(filme_id)

  return render_template('read_single.html', filme=filme)

  #Rota do Create

@bp.route('/create', methods=('GET', 'POST'))
def create():

  id_atribuido = None
#Como o método utilizado no formulário é POST, pegamos os valores dos campos
  if request.method =='POST':
    form=request.form
    filme = Filmes(form['nome'],form['imagem_url']) 
    filme.save()
    id_atribuido=filme.id
  return render_template('create.html', id_atribuido=id_atribuido)

#Rota do Update

@bp.route('/update/<filme_id>',methods=('GET', 'POST'))
def update(filme_id):
  sucesso = None
  filme = Filmes.read_single(filme_id)  

  if request.method =='POST':
    form=request.form

    new_data= Filmes(form['nome'],form['imagem_url']) 

    filme.update(new_data)

    sucesso = True

  return render_template('update.html', filme=filme,sucesso=sucesso)







# Pega os dados do blueprint da nossa aplicação (nome do app e as rotas) e registra dentro do app do Flask
app.register_blueprint(bp)


if __name__ == '__main__':
  app.run(debug=True)
