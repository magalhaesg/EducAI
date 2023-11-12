from flask import Flask, render_template, request
import openai

app = Flask(__name__)
openai.api_key = 'Inclua sua chave de API aqui'
app.jinja_env.autoescape = True
app.jinja_env.globals.update(enumerate=enumerate)
title = "A bordadeira"
text = """
Era uma vez uma bordadeira chamada Filomena que vivia com dores em seus dez dedos das mãos e em seus dois olhos. Porque desde a hora em que acordava até a hora em que se deitava para dormir, ela bordava, bordava, bordava, bordava, bordava, bordava. bordava, bordava. [...]
\nIsso acontecia porque ela bordava muito bem. Bordava táo bem, que todas as princesas daquela parte do mundo queriam ter vestidos e blusas e casaquinhos e lenços e saias e xales e até sapatos com bordados feitos pela Filomena.
\nEla vivia táo cansada que já tinha esquecido da última vez que tinha sorrido. De quando tinha dado uma risada, então, nem se fala. Gargalhada? A última que saiu de dentro dela foi quando ela ainda era uma menininha.
\nQuando se aproximou a data do aniversário da princesa do reino onde ela morava, a bordadeira foi mais requisitada que nunca, e suas mãos doeram como nunca, e seus dedos ficaram mais picados que nunca.
\nEla ficou com tanta raiva de tudo e de todos que se trancou em seu quarto de bordar, rodeada de panos, linhas e agulhas, e começou a bordar e contar para si mesma a história da princesa que engasgou com uma semente de romã e nasceu um pé de romã dentro dela e ela se transformou numa raiz e viveu muitos anos enfiada dentro da terra, há, há, há!
\nÉ claro que essa história não existia. A Filomena inventou para se vingar de todas as princesas, e entáo...
\n...de repente se sentiu táo descansada! Parecia um milagre! Estava com o corpo leve. Os dedos lisinhos. As mãos macias. Os olhos relaxados. A bordadeira soltou um longo e barulhento bocejo enquanto se espreguiçava, e sentiu vontade de sorrir, e sorriu, riu, gargalhou. Ela achou graça de uma coisa que passou pela cabeça dela. Estava com a sensaçáo absurda de que tinha dormido durante cem anos! E, com muita vontade e alegria, voltou a bordar.
\nDe repente um rapaz muito bem vestido e elegante e atlético e até um tanto formoso entrou pela janela Assim que se olharam, Filomena e esse rapaz, que era um príncipe, se apaixonaram um pelo outro."""
footer = "SOUZA, Flavio de. Que história é essa? São Paulo: Companhia dos Letrinhas, 2000 p23-23 (Fragmento)"
completed_text = title + text + footer
questions = [
    "Qual é o nome da bordadeira?",
    "Em determinado momento. Filomena quis vingar-se de todas as princesas. Por que ela queria fazer isso?",
    """Observe o trecho a seguir: 
\n"Quando se *aproximou* a data do aniversário da *princesa* do reino onde ela morava, a bordadeira foi mais requisitada que nunca..."
\n O que as duas palavras possuem em comum?"""
]

gabarito = [
    "Filomena.", 
    "Estava cansada de ter que bordar muitas roupas para as princesas.", 
    """As palavras possuem encontro consonantal."""
]

@app.route('/') #página de disciplinas
def homepage():
    return render_template('content.html')

@app.route('/login') #página login
def contatos():
    return render_template('index.html')

@app.route('/result', methods=("GET", "POST")) #página de resultado
def result():
    return render_template('result.html')

@app.route('/quiz', methods=("GET", "POST")) #página de questionário
def quiz():
    if request.method == 'POST':
        answers = []
        for i in range(len(questions)):
            user_answer = request.form.get(f'q{i}')
            answers.append(user_answer)

        # Envie as respostas para o modelo GPT-3.5
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt = f"Contexto: \n{completed_text}\n\nQuestões: \n{questions}\n\nGabarito: \n{gabarito}\n\nRespostas dos Alunos: \n{answers}\n\nAvaliação das Respostas dos Alunos:\nPor favor, avalie as respostas dos alunos em relação ao gabarito e forneça correções detalhadas, além de sugestões de melhoria caso seja necessário. Considere critérios como precisão, clareza da escrita, uso de evidências e argumentação. Cada resposta deve ser avaliada separadamente. Leve em consideração que cada aluno se expressa de maneira única, e respostas diferentes podem ser parcialmente corretas ou incorretas. Questão 1: - avaliação da resposta; Questão 2: - avaliação da resposta; ...  Questão N: avaliação da resposta;. Não esqueça, caso o aluno não saiba a resposta ajude-o a alcançá-la.",
            # prompt = f"Contexto: \n{completed_text}\n\nQuestões: \n{questions}\n\nGabarito: \n{gabarito}\n\nRespostas dos Alunos: \n{answers}\n\nAvaliação das Respostas dos Alunos:\nPor favor, avalie as respostas dos alunos em relação ao gabarito e forneça correções detalhadas, além de sugestões de melhoria caso seja necessário. Considere critérios como precisão, clareza da escrita, uso de evidências e argumentação. Cada resposta deve ser avaliada separadamente. Leve em consideração que cada aluno se expressa de maneira única, e respostas diferentes podem ser parcialmente corretas ou incorretas. Questão 1: - Avaliação e correção da resposta do aluno. Questão 2: - Avaliação e correção da resposta do aluno. ... Questão N: - Avaliação e correção da resposta do aluno. Não esqueça, caso o aluno não saiba a resposta ajude-o a alcançá-la.",
            # prompt = f"Texto de apoio:\n{completed_text}\n\nQuestões:\n{questions}\n\nGabarito:\n{gabarito}\n\nRespostas do Aluno:\n{answers}\n\nAvaliação da Resposta:\nAvalie a resposta do aluno e forneça correções detalhadas. Leve em consideração que cada aluno se expressa de maneira única, e respostas diferentes podem ser parcialmente corretas ou incorretas. Explique as razões por trás de cada correção e forneça sugestões específicas para melhoria. Certifique-se de ser completo e informativo em sua análise. Não esqueça de separar cada correção com 'Questão x'.\n\n",
            temperature=0.6,
            max_tokens=3000,
        )
        generated_answers = response.choices[0].text.split('\n')
        combined_data = zip(questions, answers)
        return render_template('result.html', user_answers=answers, generated_answers=generated_answers, combined_data=combined_data)
    generated_answers=generated_answers = request.args.get('generated_answers=generated_answers')
    return render_template('quiz.html', questions=questions, text=text.replace("\n","<br>"), title=title, footer=footer)

if __name__ == '__main__':
    app.run(debug=True)
