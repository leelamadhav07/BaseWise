from basewise.database import Database

db = Database()

try:
    db.connect()

    print("Database connected successfully!")
    print("Connected:", db.is_connected())

except Exception as e:
    print("Database connection failed!")
    print("Error:", e)

finally:
    db.close()
    print("Database connection closed.")