from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import RawImport


def create_raw_import(db: Session, line: str):
    keys = RawImport.__table__.columns.keys()
    del keys[keys.index('id')]
    del keys[keys.index('processed')]

    # Remplacer le nom de la table et les colonnes
    table_and_fields_name = f"{RawImport.__table__.name} ({', '.join(keys)})"
    line = line.replace("`x_world`", table_and_fields_name)

    # Utiliser une connexion brute pour exécuter la requête
    raw_conn = db.connection().engine.raw_connection()
    try:
        with raw_conn.cursor() as cursor:
            cursor.execute(line)
        raw_conn.commit()
    finally:
        raw_conn.close()