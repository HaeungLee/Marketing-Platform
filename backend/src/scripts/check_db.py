from sqlalchemy import inspect
from config.database import engine

def check_database():
    inspector = inspect(engine)
    
    # Get all table names
    table_names = inspector.get_table_names()
    print("\nExisting tables:")
    for table_name in table_names:
        print(f"- {table_name}")
        # Get columns for each table
        columns = inspector.get_columns(table_name)
        print("  Columns:")
        for column in columns:
            print(f"    - {column['name']} ({column['type']})")
        print()

if __name__ == "__main__":
    check_database()
