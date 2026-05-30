import sqlite3

def view_sqlite_database():
    conn = sqlite3.connect('instance/e_brokerr.db')
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    print("🔍 E BROKERR SQLITE DATABASE VIEW")
    print("=" * 50)
    print(f"Database file: instance/e_brokerr.db")
    print(f"Total tables: {len(tables)}")
    print()

    for table_name, in tables:
        print(f"📋 TABLE: {table_name}")
        print("-" * 30)

        # Get table info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"Columns ({len(columns)}):")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) {'PRIMARY KEY' if col[5] else ''}")
        print()

        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"Total rows: {count}")
        print()


        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            rows = cursor.fetchall()
            print("Sample data:")
            for i, row in enumerate(rows, 1):
                print(f"  Row {i}: {row}")
            if count > 3:
                print(f"  ... and {count - 3} more rows")
        print()

    conn.close()
    print("✅ SQLite database view complete!")

if __name__ == '__main__':
    view_sqlite_database()