# Text2Clima - Acesso a Dados Climáticos via ChatBot

![Python](https://img.shields.io/badge/Python-3.15-blue?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Data_Warehouse-informational?logo=postgresql)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-green)
![Gemini](https://img.shields.io/badge/Google_Gemini-3.5_Flash_Lite-orange?logo=google)


# Funcionamento

![til](images/text2clima.gif)

O objetivo é facilitar o acesso aos dados climáticos históricos do conjunto BR-DWGD (Brazilian Daily Weather Gridded Data), com foco inicial nas regiões produtoras de cafés especiais do Brasil. Posteriormente, outras bases rotineiramente utilizadas em pesquisas climáticas serão integradas ao projeto. 

No repositório, encontra-se a construção de uma interface que será acoplada um modelo de linguagem (LLM) para permitir consultas ao banco de dados utilizando linguagem natural.

## Contexto
A extração dos dados na íntegra ou de recortes específicos, exige conhecimento técnico em programação ou SQL.

Para eliminar esse requisito para quem tem a necessidade de utilizar esses dados, o projeto foi dividido em duas etapas: 

* A organização dos dados espalhados em um banco estruturado; 
* A criação de um tradutor  (Text-to-SQL) que entende o que o usuário quer em relação aos dados, escreve o código SQL sozinho, consulta o banco e devolve a resposta pronta. (Este repositório.)

## Engenharia de Dados
A base do projeto já está construída e populada, e o desenvolvimento dessas partes encontra-se em dois repositórios distintos ([special-coffee-climate-change [1]](https://github.com/matheus-naves47/special-coffee-climate-change) e [climate-database-sql [2]](https://github.com/matheus-naves47/climate-database-sql)):
* Extração dos dados brutos em formato NetCDF utilizando linguagem R. [1]
* Processamento e armazenamento em arquivos particionados (Parquet). [1]
* Desenvolvimento de um pipeline de ingestão em Python (usando pandas e SQLAlchemy) que trata os dados, corrige inconsistências de nomenclatura e alimenta um banco de dados PostgreSQL. [2]
* Modelagem do banco de dados separando as informações de cadastro (Regiões e Municípios) das bilhões de medições climáticas diárias (precipitação, temperaturas, evapotranspiração, etc.), garantindo alta performance nas consultas. [2]

## Desenvolvimento Atual
Atualmente, o projeto foca na construção da interface de consumo e na integração com inteligência artificial, contemplando as seguintes implementações:
* Integração com a API do Google Gemini utilizando o framework LangChain.
* Desenvolvimento de um agente Text-to-SQL que converte perguntas em português (ex: "Qual foi a média de chuva no Cerrado Mineiro no inverno de 2020?") em consultas diretas no banco de dados.
* Adoção de uma arquitetura "White-Box" (caixa branca) para o agente. A fim de contornar problemas de latência (consultas superiores a 8 minutos) causados pela reflexão automática de metadados em bancos massivos, o esquema do banco de dados foi mapeado de forma estática no prompt. Essa abordagem reduziu o tempo de resposta para cerca de 3 segundos.
* Construção de uma interface visual de chat utilizando Streamlit, para que os usuários interajam com os dados de forma fluida.
* Inclusão de um recurso de auditabilidade na interface, permitindo que o pesquisador expanda os detalhes técnicos de cada resposta para verificar a exatidão do código SQL gerado e conferir os dados brutos extraídos do PostgreSQL.

## Tecnologias Utilizadas
* **Manipulação de Dados:** R, Python, Pandas, PyArrow
* **Banco de Dados:** PostgreSQL, SQLAlchemy, psycopg2
* **Inteligência Artificial:** Google Gemini API (modelo Flash Lite), LangChain
* **Interface (Frontend):** Streamlit

## Passos para Execução 

1. **Clonar o repositório:**
```bash
git clone https://github.com/matheus-naves47/text2clima.git
cd text2clima
```

2. **Criar e ativar o ambiente virtual:**
```bash
python -m venv .env
source .env/bin/activate 
```

3. **Instalar as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configurar as variáveis de ambiente:**
No arquivo `.environment`, inserir as credenciais do banco de dados local e da API do Google.
```env
GEMINI_API_KEY="chave"
DATABASE_URL="postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco"
```

5. **Iniciar a interface gráfica:**
```bash
streamlit run src/app.py
```

