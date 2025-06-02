# UniAjuda - Plataforma de Apoio Acadêmico

## Descrição

**UniAjuda** é uma aplicação desktop em Python com interface Tkinter, criada para conectar alunos com dúvidas a colegas dispostos a ajudar. O objetivo é promover colaboração acadêmica de forma simples, eficiente e local.

## Tecnologias Utilizadas

- Python — linguagem principal
- Tkinter — interface gráfica (GUI)
- SQLite — banco de dados local
- Matplotlib — geração de gráficos
- FPDF — criação de PDFs
- Pandas — manipulação de dados

## Estrutura do Projeto

```
UNIAJUDA/
├── main.py                  # Inicialização e navegação principal da aplicação
├── database.py              # Criação e manipulação do banco de dados SQLite
├── gui/                     # Telas e componentes gráficos (Tkinter)
│   ├── login_screen.py
│   ├── register_screen.py
│   ├── recover_screen.py
│   ├── home_screen.py
│   ├── question_screen.py
│   ├── profile_screen.py
│   ├── report_screen.py
│   ├── post_question_screen.py
│   ├── answer_question_screen.py
│   └── report_screen.py
├── controllers/             # Lógica de controle e regras de negócio
│   ├── user_controller.py
│   ├── question_controller.py
│   ├── answer_controller.py
│   └── report_controller.py
├── models/                  # Modelos de dados (ORM simples)
│   ├── user.py
│   ├── question.py
│   └── answer.py
└── utils/                   # Utilitários para geração de PDF e gráficos
    ├── pdf_generator.py
    └── chart_generator.py
```

- **main.py**: Inicialização e navegação entre telas.
- **database.py**: Criação das tabelas e conexão com SQLite.
- **gui/**: Telas de login, cadastro, recuperação, home, dúvidas, respostas e relatórios.
- **controllers/**: Lógica de autenticação, dúvidas, respostas e relatórios.
- **models/**: Estruturas de dados para usuários, dúvidas e respostas.
- **utils/**: Geração de relatórios em PDF e gráficos estatísticos.

## Funcionalidades

- Cadastro e autenticação de usuários
- Postagem e organização de dúvidas por disciplina
- Respostas colaborativas de outros alunos
- Visualização de gráficos estatísticos (Matplotlib)
- Geração de relatórios em PDF

## Como Inicializar

1. Clone o repositório:
    ```bash
    git clone https://github.com/MarceloHenri250/UNIAJUDA.git
    ```
2. Acesse o diretório do projeto:
    ```bash
    cd UNIAJUDA
    ```
3. (Opcional) Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```
4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
5. Execute a aplicação:
    ```bash
    python main.py
    ```

A interface gráfica será aberta e você poderá começar a usar o UniAjuda.

## Público-Alvo

Estudantes universitários que desejam tirar dúvidas ou ajudar colegas em disciplinas específicas.

## Cenário de Uso

Um aluno posta uma dúvida sobre uma disciplina. Outro aluno visualiza e responde. Todas as interações ficam registradas e podem ser consultadas em relatórios e gráficos.

## Requisitos Funcionais

- Cadastro e autenticação de alunos
- Postagem e resposta de dúvidas
- Geração de relatórios em PDF
- Visualização de gráficos estatísticos

## Requisitos Não Funcionais

- Interface amigável e intuitiva
- Funcionamento offline
- Compatibilidade com Windows e Linux

## Entradas e Saídas

- **Entradas:** Nome, matrícula, curso, dúvidas (texto, disciplina, urgência), respostas  
- **Saídas:** Listagens de dúvidas e respostas, relatórios em PDF, gráficos por disciplina

## Etapas de Implementação

1. Estruturação do projeto e criação do banco de dados
2. Implementação das telas de login, cadastro e recuperação de senha
3. Funcionalidade de postagem e resposta de dúvidas
4. Geração de relatórios em PDF e gráficos estatísticos
5. Testes, refinamento visual e melhorias na navegação entre telas/modais

## Critérios de Validação

- Cadastro e login funcionam corretamente
- Dúvidas e respostas são armazenadas e recuperadas
- Relatórios e gráficos são gerados corretamente

---

Sinta-se à vontade para contribuir ou sugerir melhorias!
