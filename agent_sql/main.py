from prompts import MSSQL_AGENT_PREFIX, MSSQL_AGENT_FORMAT_INSTRUCTIONS

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
import pandas as pd
from sqlalchemy import create_engine
import os

from dotenv import load_dotenv
load_dotenv()

# Crie o diretório db se ele não existir
os.makedirs("./db", exist_ok=True)

file_url = "./data/all-states-history.csv"
df = pd.read_csv(file_url).fillna(value=0)

# Path to your SQLite database file
database_file_path = "./db/test.db"

# Crie um mecanismo para conectar ao banco de dados SQLite
engine = create_engine(f'sqlite:///{database_file_path}')

df.to_sql(
    'all_states_history',
    con=engine,
    if_exists='replace',
    index=False)

db = SQLDatabase.from_uri(f'sqlite:///{database_file_path}')

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com/beta",
    api_key=os.getenv("DEEP_SEEK_API_KEY"),
    temperature=0.5,
    max_tokens=1000
    )

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor_SQL = create_sql_agent(
    prefix=MSSQL_AGENT_PREFIX,
    format_instructions = MSSQL_AGENT_FORMAT_INSTRUCTIONS,
    llm=llm,
    toolkit=toolkit,
    top_k=30,
    verbose=True)

QUESTION = """
            Quantos pacientes foram hospitalizados durante outubro de 2020
            em Nova York e em todo o país como o total de todos os estados?
          """

# Execute the SQL agent
result = agent_executor_SQL.invoke(QUESTION)
print("\nRESULTADO FINAL:")
print(result["output"])