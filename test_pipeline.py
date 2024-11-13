import logging
import threading
from unittest.mock import patch
import pytest
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pipeline import transform_data, load_to_mysql, Country, Base
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))

@pytest.fixture(scope="function")
def test_engine():
    """Cria um banco de dados SQLite em memória para testes."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine) 
    return engine


@pytest.fixture(scope="function")
def test_session(test_engine):
    """Cria uma sessão SQLAlchemy para os testes."""
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()


def test_transform_data():
    """Teste para verificar a transformação dos dados."""

    data = {"codigo": ["1", "02", "003"], "nome": ["brasil", "argentina", "uruguai"]}
    df = pd.DataFrame(data)

    transformed_df = transform_data(df)

    assert list(transformed_df['codigo']) == ["001", "002", "003"]
    assert list(transformed_df['nome']) == ["Brasil", "Argentina", "Uruguai"]


def test_load_to_mysql(test_session):
    """Teste para verificar o carregamento dos dados no banco."""
    data = {"codigo": ["001", "002", "003"], "nome": ["Brasil", "Argentina", "Uruguai"]}
    df = pd.DataFrame(data)

    load_to_mysql(df, session=test_session)

    results = test_session.query(Country).all()
    assert len(results) == 3
    assert results[0].codigo == "001"
    assert results[0].nome == "Brasil"
    assert results[1].codigo == "002"
    assert results[1].nome == "Argentina"
    assert results[2].codigo == "003"
    assert results[2].nome == "Uruguai"
