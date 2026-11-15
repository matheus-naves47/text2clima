# Text2Clima - Acesso a Dados Climáticos via ChatBot

O objetivo é facilitar o acesso aos dados climáticos históricos do conjunto BR-DWGD (Brazilian Daily Weather Gridded Data), com foco inicial nas regiões produtoras de cafés especiais do Brasil. Posteriormente, outras bases rotineiramente utilizadas em pesquisas climáticas serão integradas ao projeto. 

No repositório, encontra-se a construção de uma interface que será acoplada um modelo de linguagem (LLM) para permitir consultas ao banco de dados utilizando linguagem natural.

## Contexto
A extração dos dados na íntegra ou de recortes específicos, exige conhecimento técnico em programação ou SQL.

Para eliminar esse requisito para quem tem a necessidade de utilizar esses dados, o projeto foi dividido em duas grandes etapas: 

* A organização dos dados espalhados em um banco estruturado; 
* A criação de um tradutor  (Text-to-SQL) que entende o que o pesquisador quer, escreve o código SQL sozinho, consulta o banco e devolve a resposta pronta. (Este repositório.)

## Engenharia de Dados
A base do projeto já está construída e populada, e o desenvolvimento dessas partes encontra-se em dois repositórios distintos ([special-coffee-climate-change [1]](https://github.com/matheus-naves47/special-coffee-climate-change) e [climate-database-sql [2]](https://github.com/matheus-naves47/climate-database-sql)):
* Extração dos dados brutos em formato NetCDF utilizando linguagem R. [1]
* Processamento e armazenamento em arquivos particionados (Parquet). [1]
* Desenvolvimento de um pipeline de ingestão em Python (usando pandas e SQLAlchemy) que trata os dados, corrige inconsistências de nomenclatura e alimenta um banco de dados PostgreSQL. [2]
* Modelagem do banco de dados separando as informações de cadastro (Regiões e Municípios) das bilhões de medições climáticas diárias (precipitação, temperaturas, evapotranspiração, etc.), garantindo alta performance nas consultas. [2]

## Desenvolvimento Atual
Atualmente, o projeto está na fase de construção da interface de consumo e integração com IA:
* Integração com a API do Google Gemini utilizando o framework LangChain.
* Desenvolvimento de um agente Text-to-SQL que lê o esquema do PostgreSQL criado na fase anterior e converte perguntas em português (ex: "Qual foi a média de chuva no Cerrado Mineiro no inverno de 2020?") em consultas no banco de dados.
* Construção de uma interface visual de chat utilizando Streamlit, para que os usuários interajam com os dados como se faz em um aplicativo de mensagens.

## Tecnologias Utilizadas
* **Manipulação de Dados:** R, Python, Pandas, PyArrow
* **Banco de Dados:** PostgreSQL, SQLAlchemy
* **Inteligência Artificial:** Google Gemini API, LangChain
* **Interface (Frontend):** Streamlit