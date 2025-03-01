import pandas as pd
from config import Settings
from sqlalchemy import create_engine, text
from loguru import logger

settings = Settings()

class Database:
    def __init__(self):
        self.engine = self.get_engine()
        self.connection = self.engine.connect()

    def get_engine(self):
        connection_string = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

        engine = create_engine(connection_string)
        return engine
    
    def get_columns_of_db(self, table_name: str):
        query = text(f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{table_name}';
        """)
        result = self.connection.execute(query)
        return [row[0] for row in result]

    def update_table_structure(self, table_name: str, df_columns):
        existing_columns = self.get_columns_of_db(table_name)
        missing_columns = [col for col in df_columns if col not in existing_columns]
        with self.connect() as connection:
            try:
                transaction = connection.begin()
                for column in missing_columns:
                    alter_query = text(f'ALTER TABLE {table_name} ADD COLUMN "{column}" TEXT;')
                    connection.execute(alter_query)  
                transaction.commit() 
                logger.info(f"Table {table_name} updated successfully")
            except Exception as e: 
                logger.error(f"Error updating table {table_name}: {e}") 

    def save_into_db(self, page: int, resource: str, content: dict):
        table_name = resource.split("/")[-2]
    
        df = pd.json_normalize(content)
        try:
            if page == 1:
                df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            else:
                self.update_table_structure(table_name, df.columns)
                df.to_sql(table_name, self.engine, if_exists='append', index=False)
            logger.info(f"Page {page} saved into table {table_name}")
        except Exception as e:
            logger.error(f"Error saving data into table {table_name}: {e}")