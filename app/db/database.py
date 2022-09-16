import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session, sessionmaker
import sqlalchemy.ext.declarative as dec

Base = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, pool_pre_ping=True, echo=True, connect_args={"check_same_thread": False})
    # Если установить echo=True, то в консоль будут выводиться все SQL-запросы
    # Не нужно - поставьте False
    __factory = orm.sessionmaker(bind=engine)

    from app.db import __all_models

    Base.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()