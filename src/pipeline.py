from pathlib import Path

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
import pandas as pd
from sqlalchemy import create_engine


# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "IOT-temp.csv"

# Configuração do PostgreSQL
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def carregar_dados():
    """Carrega os dados do arquivo CSV."""
    print("Carregando dados do CSV...")

    df = pd.read_csv(CSV_PATH)

    print(f"{len(df)} registros carregados.")
    return df


def tratar_dados(df):
    """Limpa e prepara os dados antes da inserção no PostgreSQL."""
    print("Tratando dados...")

    # Renomeia colunas para facilitar as consultas SQL
    df = df.rename(
        columns={
            "room_id/id": "room_id",
            "out/in": "ambiente",
        }
    )

    # Converte a coluna de data para datetime
    df["noted_date"] = pd.to_datetime(
        df["noted_date"],
        format="%d-%m-%Y %H:%M"
    )

    # Remove eventuais registros duplicados
    df = df.drop_duplicates()

    # Ordena cronologicamente as leituras
    df = df.sort_values("noted_date")

    print(f"{len(df)} registros após o tratamento.")
    return df


def conectar_banco():
    """Cria a conexão com o PostgreSQL."""
    return create_engine(DATABASE_URL)


def inserir_dados(df, engine):
    """Insere os dados tratados na tabela temperature_readings."""
    print("Inserindo dados no PostgreSQL...")

    df.to_sql(
        "temperature_readings",
        engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi",
    )

    print("Dados inseridos com sucesso.")


def main():
    """Executa todas as etapas do pipeline."""
    try:
        dados = carregar_dados()
        dados = tratar_dados(dados)

        engine = conectar_banco()
        inserir_dados(dados, engine)

        print("\nPipeline executado com sucesso!")

    except Exception as erro:
        print(f"\nErro durante a execução do pipeline: {erro}")


if __name__ == "__main__":
    main()