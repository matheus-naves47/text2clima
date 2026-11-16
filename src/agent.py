import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from sqlalchemy import create_engine, text

load_dotenv('.environment')

def extrair_texto(conteudo):
    if isinstance(conteudo, str):
        return conteudo
    elif isinstance(conteudo, list) and len(conteudo) > 0:
        if isinstance(conteudo[0], dict):
            return conteudo[0].get("text", "")
        return str(conteudo[0])
    return str(conteudo)

def text_to_sql_transparente(pergunta):
    api_key = os.getenv("GEMINI_API_KEY")
    db_uri = os.getenv("DATABASE_URL")
    
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", google_api_key=api_key)
    engine = create_engine(db_uri)
    
    # Adicionar o mapa de relacionamentos para o LLM não errar os JOINs
    # Verificar o nome das tabelas e colunas no banco de dados com o comando \d no psql
    
    esquema_banco = """
    Tabelas PostgreSQL:
    - regiao (id_regiao, nome_regiao)
    - municipio (id_municipio, nome_municipio, uf_sigla, id_regiao)
    - clima_regional (id_medicao, id_regiao, data_ref, pr_mm, tmax_c, tmin_c, eto_mm, rh_pct, rs, u2_m_s)
    - clima_municipal (id_medicao, id_municipio, data_ref, pr_mm, tmax_c, tmin_c, eto_mm, rh_pct, rs, u2_m_s)
    
    Relacionamentos (JOINs):
    - municipio.id_regiao = regiao.id_regiao
    - clima_regional.id_regiao = regiao.id_regiao
    - clima_municipal.id_municipio = municipio.id_municipio
    """
    
    # --- ETAPA 1: LLM GERA A QUERY ---
    prompt_sql = PromptTemplate.from_template(
        "Esquema:\n{schema}\n\nEscreva uma query PostgreSQL para responder: {question}\n"
        "Retorne APENAS o código SQL válido. Se a consulta puder retornar milhares de linhas brutas, utilize agregações (SUM, AVG, COUNT) ou limite a 100 resultados."
    )
    
    conteudo_bruto = llm.invoke(prompt_sql.format(schema=esquema_banco, question=pergunta)).content
    query_suja = extrair_texto(conteudo_bruto)
    query_limpa = query_suja.replace("```sql", "").replace("```", "").strip()
    
    # --- ETAPA 2: PYTHON EXECUTA NO BANCO ---
    try:
        with engine.connect() as conn:
            # Substituímos o fetchmany(10) por fetchall() para trazer todos os resultados da agregação
            resultado_bruto = conn.execute(text(query_limpa)).fetchall() 
    except Exception as e:
        # Agora o erro retorna no formato correto de dicionário para não quebrar o Streamlit
        return {
            "resposta": "Ops! A IA gerou um comando SQL inválido ou houve um erro no banco de dados. Clique em 'Ver mais detalhes.' para ver o que deu errado e tente reformular a pergunta.",
            "sql": query_limpa,
            "resultado_bruto": f"ERRO DO POSTGRESQL:\n{str(e)}"
        }
        
    # --- ETAPA 3: LLM TRADUZ ---
    prompt_resp = PromptTemplate.from_template(
        "Pergunta: {question}\nSQL: {query}\nResultado: {result}\nCrie uma resposta natural em português informando os dados encontrados."
    )
    
    conteudo_final_bruto = llm.invoke(prompt_resp.format(question=pergunta, query=query_limpa, result=resultado_bruto)).content
    resposta = extrair_texto(conteudo_final_bruto)
    
    return {
        "resposta": resposta,
        "sql": query_limpa,
        "resultado_bruto": str(resultado_bruto)
    }