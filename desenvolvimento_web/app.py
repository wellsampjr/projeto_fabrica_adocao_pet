#Importamos as bibliotecas necessárias
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime   
import json
import resend  

#Adicionando a chave da API do Resend para o envio de e-mails
resend.api_key = "re_UhHDSMSR_76JcVb4AcuRVqSh9P3DTyK82"

#Instanciamos a aplicação web
app = Flask(__name__)

with open('dados.json', 'r',encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('name')
        email = request.form.get('email')
        mensagem = request.form.get('message')

#Montar o dicionario da nova mensagem

        dados_mensagem = {
            'nome': nome,
            'email': email,
            'mensagem': mensagem,
            'data':f"{datetime.today()}"
        }

#Adicionar e salvar no JSON
        dados.append(dados_mensagem)
        with open("dados.json","w", encoding="utf-8") as arquivo:
            json.dump(dados,arquivo, indent=4, ensure_ascii=False)

#Envia e-mail usando Resend
            r=resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": "wellsamppjr@gmail.com",
                "subject": f"Solicitação de adoção{nome}",
                "html": f"<p>Email:{email}<br>{mensagem}</p>",
            })

#Após o POST, Redireciona para enviar reenvio do formulário
        return redirect(url_for('index'))


#GET - Renderiza a página
    return render_template('index.html')   


if __name__ == "__main__":
    app.run(debug=True)