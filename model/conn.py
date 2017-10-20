from sqlalchemy import create_engine
from config import MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_SERVER, MYSQL_DBNAME


_engine = None


def engine():
    global _engine
    if not _engine:
        conn_str = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4&autocommit=true".format(MYSQL_USERNAME,
                                                                                        MYSQL_PASSWORD,
                                                                                        MYSQL_SERVER,
                                                                                        MYSQL_DBNAME)
        _engine = create_engine(conn_str, pool_size=60, max_overflow=0, pool_recycle=20)
    return _engine


engine = engine()
