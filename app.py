from flask import Flask, render_template, request, redirect, url_for, flash, session
import firebase_admin
from datetime import datetime, timedelta
from firebase_admin import credentials, firestore
from werkzeug.security import generate_password_hash, check_password_hash
from google.api_core.exceptions import NotFound, GoogleAPICallError

app = Flask(__name__)
app.secret_key = 'bozo13'

cred = credentials.Certificate("reserva-livros-.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

COL_USUARIOS = 'usuarios'
COL_LIVROS = 'livros'
COL_HISTORICO = 'historico'


#home 
@app.route('/')
def home():
    usuario = session.get('usuario')
    historico = []

    if usuario:
        docs = db.collection(COL_HISTORICO) \
                 .where('usuario', '==', usuario) \
                 .where('ativo', '==', True) \
                 .limit(4) \
                 .stream()

        for doc in docs:
            dados = doc.to_dict()
            historico.append({
                'titulo': dados.get('titulo'),
                'imagem': dados.get('imagem', ''),
                'data_emprestimo': dados.get('data_emprestimo'),
                'data_devolucao': dados.get('data_devolucao')
            })

    return render_template('home.html', usuario=usuario, historico=historico)


# kadrastooo
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        senha = request.form.get('senha', '').strip()

        if nome and senha:
            doc_ref = db.collection(COL_USUARIOS).document(nome)
            if not doc_ref.get().exists:
                senha_hash = generate_password_hash(senha)
                doc_ref.set({'nome': nome, 'senha': senha_hash})
                flash("Cadastro realizado com sucesso!", "success")
                return redirect(url_for('login'))
            else:
                flash("Usuário já existe.", "error")

    return render_template('cadastro.html')


#loggin
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        senha = request.form.get('senha', '').strip()

        doc = db.collection(COL_USUARIOS).document(nome).get()

        if doc.exists:
            dados = doc.to_dict()
            if check_password_hash(dados.get('senha', ''), senha):
                session['usuario'] = nome
                flash("Login bem-sucedido!", "success")

                destino = session.pop('destino', None)
                return redirect(destino or url_for('home'))
            else:
                flash("Senha incorreta.", "error")
        else:
            flash("Usuário não encontrado.", "error")

    return render_template('login.html')


#livru
@app.route('/livros', methods=['GET', 'POST'])
def livros_view():


    if request.method == 'POST':

        if 'usuario' not in session:
            flash("Você precisa fazer login para reservar.", "warning")
            session['destino'] = url_for('livros_view')
            return redirect(url_for('login'))

        usuario = session['usuario']
        acao = request.form.get('acao')
        livro_doc_id = request.form.get('livro')

        if not livro_doc_id:
            flash("Livro não especificado.", "error")
            return redirect(url_for('livros_view'))

        livro_ref = db.collection(COL_LIVROS).document(livro_doc_id)
        livro_doc = livro_ref.get()

        if not livro_doc.exists:
            flash("O livro não existe mais.", "error")
            return redirect(url_for('livros_view'))

        livro = livro_doc.to_dict()
        estoque = livro.get('estoque', 0)
        estoque_max = livro.get('estoque_max', 10)

      
        if acao == 'reservar':
            if estoque > 0:
                novo_estoque = estoque - 1

                livro_ref.update({
                    'estoque': novo_estoque,
                    'disponivel': novo_estoque > 0,
                    'reservado_por': usuario
                })

                data_devolucao = (datetime.now() + timedelta(days=15)).strftime('%d/%m/%Y')

                db.collection(COL_HISTORICO).add({
                    'titulo': livro_doc_id,
                    'usuario': usuario,
                    'data_emprestimo': datetime.now().strftime('%d/%m/%Y'),
                    'data_devolucao': data_devolucao,
                    'imagem': livro.get('imagem', ''),
                    'ativo': True
                })

                flash(f"Você reservou '{livro_doc_id}'.", "success")

            else:
                flash("Livro indisponível.", "error")

   
        elif acao == 'devolver':
            if livro.get('reservado_por') != usuario:
                flash("Você não pode devolver um livro que não reservou.", "error")
                return redirect(url_for('livros_view'))

            novo_estoque = min(estoque + 1, estoque_max)

            livro_ref.update({
                'estoque': novo_estoque,
                'disponivel': True,
                'reservado_por': None
            })

     
            historico_query = db.collection(COL_HISTORICO) \
                .where('usuario', '==', usuario) \
                .where('titulo', '==', livro_doc_id) \
                .where('ativo', '==', True) \
                .stream()

            for h in historico_query:
                h.reference.update({'ativo': False})

            flash(f"Você devolveu '{livro_doc_id}'.", "success")

 
        elif acao == 'cancelar':
            if livro.get('reservado_por') != usuario:
                flash("Você não pode cancelar uma reserva que não é sua.", "error")
                return redirect(url_for('livros_view'))

            novo_estoque = min(estoque + 1, estoque_max)

            livro_ref.update({
                'estoque': novo_estoque,
                'disponivel': True,
                'reservado_por': None
            })

            historico_query = db.collection(COL_HISTORICO) \
                .where('usuario', '==', usuario) \
                .where('titulo', '==', livro_doc_id) \
                .where('ativo', '==', True) \
                .stream()

            for h in historico_query:
                h.reference.update({'ativo': False})

            flash(f"Reserva de '{livro_doc_id}' cancelada.", "success")

        return redirect(url_for('livros_view'))

 
    livros_docs = db.collection(COL_LIVROS).stream()
    livros = []

    for doc in livros_docs:
        d = doc.to_dict()
        d['doc_id'] = doc.id
        d['titulo'] = d.get('titulo', doc.id)
        d['imagem'] = d.get('imagem', '')
        d['estoque'] = d.get('estoque', 0)
        d['disponivel'] = d['estoque'] > 0
        livros.append(d)

    usuario = session.get('usuario')

    return render_template('livros.html', livros=livros, usuario=usuario)



# historiccc

@app.route('/historico')
def historico_view():
    if 'usuario' not in session:
        flash("Faça login para ver seu histórico.", "warning")
        return redirect(url_for('login'))

    usuario = session['usuario']

    docs = db.collection(COL_HISTORICO) \
             .where('usuario', '==', usuario) \
             .stream()

    historico = []
    for doc in docs:
        d = doc.to_dict()
        historico.append(d)

    return render_template('historico.html', historico=historico)








@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você saiu da conta.", "success")
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)
