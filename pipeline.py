import pandas as pd
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import logging


# Configuração do banco de dados
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/countries_db"

logging.basicConfig(
    level=logging.INFO,  # Define o nível de log (INFO, DEBUG, etc.)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

Base = declarative_base()

class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(3), nullable=False, unique=True)
    nome = Column(String(255), nullable=False)

def init_db():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    return engine

engine = init_db()
Session = sessionmaker(bind=engine)

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_csv(file_path: str) -> pd.DataFrame:
    """Extrai dados de um arquivo CSV."""
    df = pd.read_csv(file_path, delimiter=";", names=["codigo", "nome"])
    return df

@task
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma os dados, limpando e validando."""
    # Removendo linhas inválidas
    df = df.dropna()
    # Normalizando os códigos e nomes
    df['codigo'] = df['codigo'].str.zfill(3)  # Garantir que os códigos tenham 3 dígitos
    df['nome'] = df['nome'].str.title()  # Formatando nomes com título
    return df

@task
def load_to_mysql(df: pd.DataFrame, session=None):
    """Carrega os dados para o MySQL utilizando SQLAlchemy."""
    if session is None:
        # Cria uma nova sessão padrão caso não seja passada
        Session = sessionmaker(bind=engine)
        session = Session()

    for _, row in df.iterrows():
        # Inserindo ou ignorando duplicatas
        country = session.query(Country).filter_by(codigo=row['codigo']).first()
        if not country:
            new_country = Country(codigo=row['codigo'], nome=row['nome'])
            session.add(new_country)
    session.commit()
    session.close()


@flow
def etl_pipeline(file_path: str):
    """Pipeline de ETL completo."""
    data = extract_csv(file_path)
    transformed_data = transform_data(data)
    load_to_mysql(transformed_data)

if __name__ == "__main__":
    csv_file_path = "paises.csv"
    etl_pipeline(csv_file_path)
