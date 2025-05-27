# UniAjuda - Plataforma de Apoio Acadêmico

## 📚 Descrição

**UniAjuda** é uma aplicação desktop em Python com interface Tkinter, criada para conectar alunos com dúvidas a colegas dispostos a ajudar. O objetivo é promover colaboração acadêmica de forma simples, eficiente e local.

## 🧰 Tecnologias Utilizadas

- **Python** — linguagem principal
- **Tkinter** — interface gráfica (GUI)
- **SQLite** — banco de dados local
- **Matplotlib** — geração de gráficos
- **FPDF** — criação de PDFs
- **Pandas** — manipulação de dados

## 📁 Estrutura do Projeto

```
UNIAJUDA/
├── main.py
├── database.py
├── gui/
│   ├── __init__.py
│   ├── login_screen.py
│   ├── home_screen.py
│   ├── post_question_screen.py
│   ├── answer_question_screen.py
│   └── report_screen.py
├── controllers/
│   ├── __init__.py
│   ├── user_controller.py
│   ├── question_controller.py
│   └── report_controller.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── question.py
│   └── answer.py
└── utils/
    ├── __init__.py
    ├── pdf_generator.py
    └── chart_generator.py
```
- **main.py**: Inicialização da aplicação.

## 🎯 Funcionalidades

- Cadastro e autenticação de usuários
- Postagem e organização de dúvidas por disciplina
- Respostas colaborativas de outros alunos
- Visualização de gráficos estatísticos (Matplotlib)
- Geração de relatórios em PDF

## 🚀 Como Inicializar

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/MarceloHenri250/UNIAJUDA.git
    ```
2. **Acesse o diretório do projeto:**
    ```bash
    cd UNIAJUDA
    ```
3. **(Opcional) Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```
4. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
5. **Execute a aplicação:**
    ```bash
    python main.py
    ```

A interface gráfica será aberta e você poderá começar a usar o UniAjuda.

## 👥 Público-Alvo

Estudantes universitários que desejam tirar dúvidas ou ajudar colegas em disciplinas específicas.

## 📝 Cenário de Uso

Um aluno posta uma dúvida sobre uma disciplina. Outro aluno visualiza e responde. Todas as interações ficam registradas e podem ser consultadas em relatórios e gráficos.

## ✅ Requisitos Funcionais

- Cadastro e autenticação de alunos
- Postagem e resposta de dúvidas
- Geração de relatórios em PDF
- Visualização de gráficos estatísticos

## ⚙️ Requisitos Não Funcionais

- Interface amigável e intuitiva
- Funcionamento offline
- Compatibilidade com Windows e Linux

## 🔄 Entradas e Saídas

- **Entradas:** Nome, matrícula, curso, dúvidas (texto, disciplina, urgência), respostas  
- **Saídas:** Listagens de dúvidas e respostas, relatórios em PDF, gráficos por disciplina

## 🛠️ Etapas de Implementação

1. Estrutura inicial e login
2. Postagem de dúvidas
3. Respostas e banco de dados
4. Relatórios e gráficos
5. Testes e refinamento visual

## 🧪 Critérios de Validação

- Cadastro e login funcionam corretamente
- Dúvidas e respostas são armazenadas e recuperadas
- Relatórios e gráficos são gerados corretamente

---

Sinta-se à vontade para contribuir ou sugerir melhorias!
