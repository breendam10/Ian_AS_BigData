# 🏫 Chatbot de atendimento ao aluno

### ⚙ Projeto desenvolvido por **Ian Esteves**

Este projeto constitui um **Chatbot inteligente** que permite usuários a realizarem mátricula, executar consultas e tirarem dúvidas de forma rápida e intuitiva.

---

### 🌐 API (Web App no Azure)

**MÉTODOS**:
- ✅ **POST /api/matriculas/** - Cria o cadastro de um aluno
```
{
"nome": "Brenda Mendes",
"email": "brendinha@email.com",
"curso": "Ciência de Dados"
}
```
- 🔍 **GET /api/matriculas/** - Retorna o cadastrado de todos os alunos
```
[
    {
        "curso": "Ciência de Dados",
        "email": "brendinha@email.com",
        "matricula": "202501027867",
        "nome": "Brenda Mendes"
    },
    {
        "curso": "Ciência de Dados",
        "email": "ianesteves@email.com",
        "matricula": "202501962104",
        "nome": "Ian Esteves"
    }
]
```
- 🔍 **GET /api/matriculas/{matricula}** - Retorna o cadastro de um aluno pela sua Matrícula
```
{
    "curso": "Ciência de Dados",
    "email": "ianesteves@email.com",
    "matricula": "202501962104",
    "nome": "Ian Esteves"
}
```
---

## 👨‍💻 Tecnologias Utilizadas

- **Python - Flask**
- **Microsoft Bot Framework**
- **Azure Web App**
- **Azure MySQL Flexible Database**
- **GitHub Actions**
