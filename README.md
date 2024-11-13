
# Projeto de Pipeline ETL para Processamento de CSV

Este projeto implementa uma pipeline **ETL (Extract, Transform, Load)** para processar um arquivo CSV contendo informações sobre países, transformar os dados no formato necessário e carregá-los em um banco de dados MySQL.

A pipeline realiza as seguintes tarefas:
- Lê um arquivo CSV local.
- Realiza transformações nos dados (normalização e validação).
- Insere os dados transformados em um banco de dados MySQL.

---

## Estrutura do Projeto

```
/seu-projeto/
├── pipeline_csv.py         # Arquivo principal da pipeline
├── paises.csv              # Arquivo CSV com os dados de entrada
├── test_pipeline_csv.py    # Testes automatizados
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação
```

---

## Funcionalidades

1. **Leitura do CSV**: O arquivo CSV deve ter a seguinte estrutura:
   - `codigo`: Código do país.
   - `nome`: Nome do país.

   Exemplo de arquivo `paises.csv`:
   ```
   "000";"COLIS POSTAUX"
   "001";"AFEGANISTAO"
   "002";"ALBANIA"
   ```

2. **Transformação dos Dados**:
   - Normaliza o código para que tenha 3 dígitos.
   - Capitaliza o nome do país.

3. **Carregamento no Banco de Dados**:
   - Insere os dados transformados em uma tabela MySQL.

---

## Pré-requisitos

- Python 3.10+
- Banco de Dados MySQL
- Dependências listadas no arquivo `requirements.txt`

---

## Como Configurar o Ambiente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o banco de dados MySQL:
   - Crie o banco de dados `countries_db`:

```sql
CREATE DATABASE countries_db;
```

- Certifique-se de que as credenciais no `pipeline_csv.py` estão corretas:

```python
DATABASE_URL = "mysql+mysqlconnector://usuario:senha@localhost/countries_db"
```

---

## Como Executar a Pipeline

1. Certifique-se de que o arquivo `paises.csv` está no diretório do projeto.
2. Execute o script principal:

```bash
python pipeline_csv.py
```

3. O script realizará as seguintes etapas:
   - Lerá os dados do arquivo `paises.csv`.
   - Transformará os dados para o formato adequado.
   - Inserirá os dados no banco de dados MySQL.

---

## Como Testar

Os testes automatizados utilizam **pytest**. Para executá-los:

```bash
pytest test_pipeline_csv.py
```

Os testes incluem:
- Validação da leitura do arquivo CSV.
- Testes de transformação dos dados.
- Inserção dos dados em um banco de dados SQLite em memória.

---

## Estrutura do Banco de Dados

A tabela criada no banco de dados MySQL é:

| **Campo**    | **Tipo**     | **Descrição**                  |
|--------------|--------------|--------------------------------|
| `id`         | `INT`        | Chave primária, autoincremento |
| `codigo`     | `VARCHAR(3)` | Código do país (3 dígitos)     |
| `nome`       | `VARCHAR(255)`| Nome do país                  |

---

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **SQLAlchemy**: Para interação com o banco de dados.
- **MySQL**: Banco de dados relacional.
- **pytest**: Para testes automatizados.

---

## Autor

Desenvolvido por [Cosme Sousa](https://github.com/cosmess).

---
