import pyodbc
import time
from lst import fish_table, vege_table, oth_table, fruits_table, rice_table  # Your updated function that returns (date, df)
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv()) # read local .env file

MAX_RETRIES = 3
RETRY_DELAY = 5

def execute_with_retry(query, values=None):
    for attempt in range(MAX_RETRIES):
        try:
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            return  # Success
        except (pyodbc.OperationalError, pyodbc.InterfaceError) as e:
            print(f"Error: {e}")
            if "timed out" in str(e).lower() or isinstance(e, pyodbc.InterfaceError):
                print(f"Retrying in {RETRY_DELAY} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
            else:
                raise
    raise Exception("Failed after multiple retries due to timeout or connection issues.")


conn_str = os.getenv("CONNECTION_STRING")
cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()

def write_sql_vege():
    vege_dataframes = vege_table()
    print(f"len of vege_dataframes is {len(vege_dataframes)}")
    # Create table with Date column and composite primary key (Fish, Date)
    create_table_query = """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'vegetables')
    BEGIN
        CREATE TABLE dbo.vegetables (
            [Date] INT NOT NULL,
            [Vege] NVARCHAR(255) NOT NULL,
            [Rate] NVARCHAR(10),
            [w-ptth-Yesterday] FLOAT,
            [w-ptth-Today] FLOAT,
            [w-dbll-Yesterday] FLOAT,
            [w-dbll-Today] FLOAT,
            [r-ptth-yesterday] FLOAT,
            [r-ptth-today] FLOAT,
            [r-dbll-yesterday] FLOAT,
            [r-dbll-today] FLOAT,
            [r-nara-yesterday] FLOAT,
            [r-nara-today] FLOAT,
            CONSTRAINT PK_vege PRIMARY KEY ([Vege], [Date])
        );
    END
    """
    execute_with_retry(create_table_query)

    def safe_float(value):
        if value is None:
            return 0  
        try:
            return float(value.replace(",", ""))
        except Exception:
            return None  

    for date, df in vege_dataframes:
        for idx, row in df.iterrows():
            row_data = list(row)
            # Pad the row to 12 columns (after 'Rate') if it's too short
            while len(row_data) < 12:
                row_data.append(None)
            
            check_query = "SELECT 1 FROM dbo.vegetables WHERE [Date] = ? AND [Vege] = ?"
            
            try:
                execute_with_retry(check_query, (date, row_data[0]))
                if cursor.fetchone():
                    continue
            except Exception as e:
                print(f"Skipping due to error on check: {e}")
                continue

            values = (
                    date,
                    row_data[0],
                    row_data[1],
                    safe_float(row_data[2]),
                    safe_float(row_data[3]),
                    safe_float(row_data[4]),
                    safe_float(row_data[5]),
                    safe_float(row_data[6]),
                    safe_float(row_data[7]),
                    safe_float(row_data[8]),
                    safe_float(row_data[9]),
                    safe_float(row_data[10]),
                    safe_float(row_data[11])
                )

            query = """
            INSERT INTO dbo.vegetables ([Date], [Vege], [Rate], [w-ptth-Yesterday], [w-ptth-Today],
                [w-dbll-Yesterday], [w-dbll-Today], [r-ptth-yesterday], [r-ptth-today], [r-dbll-yesterday], [r-dbll-today],
                [r-nara-yesterday], [r-nara-today])
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            try:
                execute_with_retry(query, values)
            except Exception as e:
                print(f"Failed to insert row {row_data[0]} for date {date}: {e}")
                continue

    try:
        cnxn.commit()
        print("All vege data with dates inserted successfully!")
    except Exception as e:
        print(f"Commit failed: {e}")

def write_sql_oth():
    oth_dataframes = oth_table()
    # Create table with Date column and composite primary key (Fish, Date)
    create_table_query = """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'other')
    BEGIN
        CREATE TABLE dbo.other (
            [Date] INT NOT NULL,
            [Oth] NVARCHAR(255) NOT NULL,
            [Rate] NVARCHAR(10),
            [w-ptth-Yesterday] FLOAT,
            [w-ptth-Today] FLOAT,
            [w-dbll-Yesterday] FLOAT,
            [w-dbll-Today] FLOAT,
            [r-ptth-yesterday] FLOAT,
            [r-ptth-today] FLOAT,
            [r-dbll-yesterday] FLOAT,
            [r-dbll-today] FLOAT,
            [r-nara-yesterday] FLOAT,
            [r-nara-today] FLOAT,
            CONSTRAINT PK_oth PRIMARY KEY ([Oth], [Date])
        );
    END
    """

    execute_with_retry(create_table_query)

    def safe_float(value):
        if value is None:
            return 0  
        try:
            return float(value.replace(",", ""))
        except Exception:
            return None  

    for date, df in oth_dataframes:
        for idx, row in df.iterrows():
            row_data = list(row)
            # Pad the row to 12 columns (after 'Rate') if it's too short
            while len(row_data) < 12:
                row_data.append(None)

            check_query = """
            SELECT 1 FROM dbo.other WHERE [Date] = ? AND [Oth] = ?
            """
            try:
                execute_with_retry(check_query, (date, row_data[0]))
                if cursor.fetchone():
                    continue
            except Exception as e:
                print(f"Skipping due to error on check: {e}")
                continue

            values = (
                date,
                row_data[0], 
                row_data[1],  
                safe_float(row_data[2]),
                safe_float(row_data[3]),
                safe_float(row_data[4]),
                safe_float(row_data[5]),
                safe_float(row_data[6]),
                safe_float(row_data[7]),
                safe_float(row_data[8]),
                safe_float(row_data[9]),
                safe_float(row_data[10]),
                safe_float(row_data[11])
            )

            query = """
            INSERT INTO dbo.other ([Date], [Oth], [Rate], [w-ptth-Yesterday], [w-ptth-Today],
                [w-dbll-Yesterday], [w-dbll-Today], [r-ptth-yesterday], [r-ptth-today], [r-dbll-yesterday], [r-dbll-today],
                [r-nara-yesterday], [r-nara-today])
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            try:
                execute_with_retry(query, values)
            except Exception as e:
                print(f"Failed to insert row {row_data[0]} for date {date}: {e}")
                continue

    try:
        cnxn.commit()
        print("All other data with dates inserted successfully!")
    except Exception as e:
        print(f"Commit failed: {e}")

def write_sql_fruits():
    """ghjgjhg
    """
    fruits_dataframes = fruits_table()
    # Create table with Date column and composite primary key (Fish, Date)
    create_table_query = """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'fruits')
    BEGIN
        CREATE TABLE dbo.fruits (
            [Date] INT NOT NULL,
            [Fruits] NVARCHAR(255) NOT NULL,
            [Rate] NVARCHAR(10),
            [w-ptth-Yesterday] FLOAT,
            [w-ptth-Today] FLOAT,
            [w-dbll-Yesterday] FLOAT,
            [w-dbll-Today] FLOAT,
            [r-ptth-yesterday] FLOAT,
            [r-ptth-today] FLOAT,
            [r-dbll-yesterday] FLOAT,
            [r-dbll-today] FLOAT,
            [r-nara-yesterday] FLOAT,
            [r-nara-today] FLOAT,
            CONSTRAINT PK_fruits PRIMARY KEY ([Fruits], [Date])
        );
    END
    """
    execute_with_retry(create_table_query)

    def safe_float(value):
        if value is None:
            return 0  
        try:
            return float(value.replace(",", ""))
        except Exception:
            return None  

    for date, df in fruits_dataframes:
        for idx, row in df.iterrows():
            row_data = list(row)
            # Pad the row to 12 columns (after 'Rate') if it's too short
            while len(row_data) < 12:
                row_data.append(None)

            check_query = """
            SELECT 1 FROM dbo.fruits WHERE [Date] = ? AND [Fruits] = ?
            """
            try:
                execute_with_retry(check_query, (date, row_data[0]))
                if cursor.fetchone():
                    continue
            except Exception as e:
                print(f"Skipping due to error on check: {e}")
                continue 

            values = (
                date,
                row_data[0], 
                row_data[1],  
                safe_float(row_data[2]),
                safe_float(row_data[3]),
                safe_float(row_data[4]),
                safe_float(row_data[5]),
                safe_float(row_data[6]),
                safe_float(row_data[7]),
                safe_float(row_data[8]),
                safe_float(row_data[9]),
                safe_float(row_data[10]),
                safe_float(row_data[11])
            )

            query = """
            INSERT INTO dbo.fruits ([Date], [Fruits], [Rate], [w-ptth-Yesterday], [w-ptth-Today],
                [w-dbll-Yesterday], [w-dbll-Today], [r-ptth-yesterday], [r-ptth-today], [r-dbll-yesterday], [r-dbll-today],
                [r-nara-yesterday], [r-nara-today])
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            try:
                execute_with_retry(query, values)
            except Exception as e:
                print(f"Failed to insert row {row_data[0]} for date {date}: {e}")
                continue

    try:
        cnxn.commit()
        print("All fruits data with dates inserted successfully!")
    except Exception as e:
        print(f"Commit failed: {e}")

def write_sql_rice():
    rice_dataframes = rice_table()
    # Create table with Date column and composite primary key (Fish, Date)
    create_table_query = """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'rice')
    BEGIN
        CREATE TABLE dbo.rice (
            [Date] INT NOT NULL,
            [Rice] NVARCHAR(255) NOT NULL,
            [Rate] NVARCHAR(10),
            [w-ptth-Yesterday] FLOAT,
            [w-ptth-Today] FLOAT,
            [w-mrghmll-Yesterday] FLOAT,
            [w-mrghmll-Today] FLOAT,
            [r-ptth-yesterday] FLOAT,
            [r-ptth-today] FLOAT,
            [r-dbll-yesterday] FLOAT,
            [r-dbll-today] FLOAT,
            [r-nara-yesterday] FLOAT,
            [r-nara-today] FLOAT,
            CONSTRAINT PK_rice PRIMARY KEY ([Rice], [Date])
        );
    END
    """
    execute_with_retry(create_table_query)

    def safe_float(value):
        if value is None:
            return 0  
        try:
            return float(value.replace(",", ""))
        except Exception:
            return None  

    for date, df in rice_dataframes:
        for idx, row in df.iterrows():
            row_data = list(row)
            # Pad the row to 12 columns (after 'Rate') if it's too short
            while len(row_data) < 12:
                row_data.append(None)

            check_query = """
            SELECT 1 FROM dbo.rice WHERE [Date] = ? AND [Rice] = ?
            """
            try:
                execute_with_retry(check_query, (date, row_data[0]))
                if cursor.fetchone():
                    continue
            except Exception as e:
                print(f"Skipping due to error on check: {e}")
                continue 

            values = (
                date,
                row_data[0], 
                row_data[1],  
                safe_float(row_data[2]),
                safe_float(row_data[3]),
                safe_float(row_data[4]),
                safe_float(row_data[5]),
                safe_float(row_data[6]),
                safe_float(row_data[7]),
                safe_float(row_data[8]),
                safe_float(row_data[9]),
                safe_float(row_data[10]),
                safe_float(row_data[11])
            )

            query = """
            INSERT INTO dbo.rice ([Date], [Rice], [Rate], [w-ptth-Yesterday], [w-ptth-Today],
                [w-mrghmll-Yesterday], [w-mrghmll-Today], [r-ptth-yesterday], [r-ptth-today], [r-dbll-yesterday], [r-dbll-today],
                [r-nara-yesterday], [r-nara-today])
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            try:
                execute_with_retry(query, values)
            except Exception as e:
                print(f"Failed to insert row {row_data[0]} for date {date}: {e}")
                continue

    try:
        cnxn.commit()
        print("All rice data with dates inserted successfully!")
    except Exception as e:
        print(f"Commit failed: {e}")

def write_sql_fish():
    fish_dataframes = fish_table()
    # Create table with Date column and composite primary key (Fish, Date)
    create_table_query = """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'fish')
    BEGIN
        CREATE TABLE dbo.fish (
            [Date] INT NOT NULL,
            [Fish] NVARCHAR(255) NOT NULL,
            [Rate] NVARCHAR(10),
            [w-plygd-Yesterday] FLOAT,
            [w-plygd-Today] FLOAT,
            [w-neg-Yesterday] FLOAT,
            [w-neg-Today] FLOAT,
            [r-neg-yesterday] FLOAT,
            [r-neg-today] FLOAT,
            [r-nara-yesterday] FLOAT,
            [r-nara-today] FLOAT,
            CONSTRAINT PK_fish PRIMARY KEY ([Fish], [Date])
        );
    END
    """
    execute_with_retry(create_table_query)

    def safe_float(value):
        if value is None:
            return 0  
        try:
            return float(value.replace(",", ""))
        except Exception:
            return None  

    for date, df in fish_dataframes:
        for idx, row in df.iterrows():
            row_data = list(row)
            # Pad the row to 12 columns (after 'Rate') if it's too short
            while len(row_data) < 12:
                row_data.append(None)

            check_query = """
            SELECT 1 FROM dbo.fish WHERE [Date] = ? AND [Fish] = ?
            """
            try:
                execute_with_retry(check_query, (date, row_data[0]))
                if cursor.fetchone():
                    continue
            except Exception as e:
                print(f"Skipping due to error on check: {e}")
                continue

            values = (
                date,
                row_data[0], 
                row_data[1],  
                safe_float(row_data[2]),
                safe_float(row_data[3]),
                safe_float(row_data[4]),
                safe_float(row_data[5]),
                safe_float(row_data[6]),
                safe_float(row_data[7]),
                safe_float(row_data[8]),
                safe_float(row_data[9])
            )

            query = """
            INSERT INTO dbo.fish ([Date], [Fish], [Rate], [w-plygd-Yesterday], [w-plygd-Today],
                [w-neg-Yesterday], [w-neg-Today], [r-neg-yesterday], [r-neg-today],
                [r-nara-yesterday], [r-nara-today])
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            try:
                execute_with_retry(query, values)
            except Exception as e:
                print(f"Failed to insert row {row_data[0]} for date {date}: {e}")
                continue

    try:
        cnxn.commit()
        print("All fish data with dates inserted successfully!")
    except Exception as e:
        print(f"Commit failed: {e}")