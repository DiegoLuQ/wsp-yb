import pymysql
import uuid


class DatabaseManager:
    def __init__(self):
        self.databases = [
            {
                "type": "mysql", "connection_str": {"host": "localhost", "user": "root", "password": "", "db": "wsp_sf", "charset": "utf8mb4"}},
                {'type': 'dynamodb', 'connection_str': {'region_name':'us-east-1', 'aws_access_key_id':'AKIAYKD2PK23BETDJ6GZ', 'aws_secret_access_key':'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'}}
        ]

    def connect(self, db_type):
        db = next((db for db in self.databases if db['type'] == db_type), None)

        if db is None:
            print(f"No database of type {db_type} found")
            return None

        if db_type == 'mysql':
            print("db_conectado")
            conn = pymysql.connect(**db['connection_str'])
            return conn

    def disconnect(self, db_type, conn):
        print("disconnect")
        if db_type == 'mysql':
            conn.close()
        else:
            pass

    def create_ticket(self, db_type, conn, ticket_id, status, created_at, number, name, description):
        if db_type == 'mysql':
            cur = conn.cursor()

            query = f"INSERT INTO tickets (ticket_id, status, created_at, number, name, description) VALUE('{ticket_id}','{status}','{created_at}','{number}','{name}','{description}')"
            cur.execute(query)
            conn.commit()
            cur.close()
        
    def get_ticket(self, db_type, conn, ticket_id):
        if db_type == 'mysql':

            cur = conn.cursor()
            query = f"SELECT status FROM tickets WHERE ticket_id = '{ticket_id}'"
            print("get_ticket")
            cur.execute(query)
            result = cur.fetchone()
            cur.close()
            return result[0]
    
    def update_ticket(self, db_type, conn, ticket_id, description):
        if db_type == 'mysql':
            cur = conn.cursor()
            query = f"UPDATE tickets SET description = '{description}' WHERE ticket_id = '{ticket_id}'"
            cur.execute(query)
            conn.commit()
            update_rows = cur.rowcount
            cur.close()
            return update_rows > 0 #devolver true si se actualizó el ticket
        
    def generate_next_ticket(self, db_type, conn):
        last_ticket_id = ''
        if db_type == 'mysql':
            cur = conn.cursor()
            query = "SELECT ticket_id FROM tickets ORDER BY ticket_id DESC LIMIT 1"
            cur.execute(query)
            result = cur.fetchone()
            last_ticket_id = result[0] if result else "TKT000"

            cur.close()

            
        
        last_number = int(last_ticket_id[3:])
        next_number = last_number + 1
        next_ticket_id = f"TKT{str(next_number).zfill(3)}"
        return next_ticket_id