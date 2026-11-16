import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase

load_dotenv('.environment')

def get_database():
    db_uri = os.getenv("DATABASE_URL")
    if not db_uri:
        raise ValueError("A variável DATABASE_URL não foi encontrada.")
    
    engine = create_engine(db_uri)
    
    # Restringir a leitura estritamente às tabelas presentes no BR-DWGD com o parâmetro include_tables
    db = SQLDatabase(
        engine,
        include_tables=["regiao", "municipio", "clima_regional", "clima_municipal"],
        sample_rows_in_table_info=0  # Evita ler dados de exemplo, apenas o esquema
    )
    
    return db