# WorkoutAPI 🏋️

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-05998b?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-d71f00?style=for-the-badge&logo=sqlalchemy)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-336791?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-24-2496ED?style=for-the-badge&logo=docker)

## 📝 Sobre o Projeto

A **WorkoutAPI** é uma API RESTful para gerenciar competições de crossfit, desenvolvida para unificar duas paixões: codificar e treinar. Este projeto, embora simplificado, aborda os conceitos essenciais para construir APIs robustas e prontas para produção com FastAPI.

O **FastAPI** é um framework web moderno e de alta performance para construção de APIs com Python, baseado nos *type hints* padrões da linguagem. Seu design assíncrono permite que a aplicação gerencie operações de I/O (como consultas ao banco de dados) de forma eficiente, sem bloquear a execução principal.

## 📊 Modelagem de Entidade e Relacionamento (MER)

A estrutura do banco de dados foi planejada para suportar as entidades principais de uma competição: atletas, categorias e centros de treinamento.

![MER](/mer.png "Modelagem de entidade e relacionamento")

## 🛠️ Stack de Tecnologias

A API foi desenvolvida utilizando as seguintes ferramentas:

-   **Linguagem:** Python 3.13
-   **Framework:** FastAPI (com código assíncrono)
-   **Banco de Dados:** PostgreSQL (gerenciado com Docker)
-   **ORM:** SQLAlchemy
-   **Migrações:** Alembic
-   **Validação de Dados:** Pydantic
-   **Ambiente Virtual:** uv

## ⚙️ Como Executar o Projeto

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

-   Python 3.13 ou superior
-   [uv](https://github.com/astral-sh/uv) (recomendado para gerenciar a versão do Python)
-   [Docker](https://www.docker.com/get-started) e [Docker Compose](https://docs.docker.com/compose/install/)

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/notilieso/dio-santander-workout-api.git
    cd dio-santander-workout-api
    ```

2.  **Crie e ative o ambiente virtual com `uv` e instale as dependências:**
    ```bash
    uv sync
    ```

3.  **Suba o container do banco de dados com Docker:**
    ```bash
    make run-postgres
    ```

5.  **Execute as migrações para criar as tabelas no banco:**
    ```bash
    make run-migrations
    ```
    > Para criar uma nova migration, use: `make create-migrations m="nome_da_sua_migration"`

6.  **Inicie o servidor da API:**
    ```bash
    make run
    ```

A API estará disponível em `http://127.0.0.1:8000`. A documentação interativa (Swagger UI) pode ser acessada em `http://127.0.0.1:8000/docs`.

## 📋 Endpoints da API

A seguir estão detalhados os endpoints disponíveis na API.

### Atletas (`/atletas/`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Retorna todos os atletas. |
| `POST` | `/` | Cria um novo atleta. |
| `GET` | `/{id}` | Retorna um atleta específico pelo seu ID. |
| `PATCH` | `/{id}` | Atualiza dados de um atleta pelo seu ID. |
| `DELETE` | `/{id}` | Deleta um atleta pelo seu ID. |

### Categorias (`/categorias/`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Retorna todas as categorias. |
| `POST` | `/` | Cria uma nova categoria. |
| `GET` | `/{id}` | Retorna uma categoria específica pelo seu ID. |

### Centros de Treinamento (`/centros_treinamento/`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Retorna todos os centros de treinamento. |
| `POST` | `/` | Cria um novo centro de treinamento. |
| `GET` | `/{id}` | Retorna um centro de treinamento específico pelo seu ID. |

## 🎯 Desafio Final (Próximos Passos)

-   [x] **Adicionar Query Parameters** nos endpoints de Atleta:
    -   Filtrar por `nome`.
    -   Filtrar por `cpf`.
-   [x] **Customizar a Resposta** do endpoint `GET /atletas`:
    -   Retornar apenas `nome`, `centro_treinamento` e `categoria`.
-   [x] **Manipular Exceção de Integridade de Dados** (`IntegrityError`):
    -   Ao tentar cadastrar um CPF já existente, retornar `status_code: 303` com a mensagem: “Já existe um atleta cadastrado com o cpf: X”.
-   [x] **Adicionar Paginação**:
    -   Implementar paginação com `limit` e `offset` utilizando a biblioteca `fastapi-pagination`.
        Foi implementado de forma manual a paginação.

## 📚 Referências

-   Documentação do FastAPI
-   Documentação do Pydantic
-   Documentação do SQLAlchemy
-   Documentação do Alembic