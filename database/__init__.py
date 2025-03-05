from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

engine = create_engine('mysql://root:admin@localhost:3306')

run_dump_first = False
if run_dump_first:
    # Read the SQL script
    script_path = 'database/dumps/Dump20240630.sql'
    try:
        with open(script_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
            print(sql_script)
    except UnicodeDecodeError as e:
        print(f"Error reading the file: {e}")
        exit(1)

    # Execute the script
    with engine.connect() as connection:
        try:
            # Use SQLAlchemy's text() for running raw SQL
            connection.execute(text(sql_script))
            print("SQL script executed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

Session = sessionmaker(bind=engine)

Base = automap_base()
Base.prepare(autoload_with=engine, schema="univercity")
