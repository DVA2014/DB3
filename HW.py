import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="clients_db",  
        user="postgres",
        password="postgres",  
        host="localhost",  
        port="5432" 
    )

def create_database():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        email VARCHAR(255) UNIQUE
    )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
        phone VARCHAR(15)
    )
    ''')

    conn.commit()
    cur.close()
    conn.close()

def add_client(first_name, last_name, email):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
    INSERT INTO clients (first_name, last_name, email) 
    VALUES (%s, %s, %s)
    ''', (first_name, last_name, email))

    conn.commit()
    cur.close()
    conn.close()

def add_phone(client_id, phone):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
    INSERT INTO phones (client_id, phone) 
    VALUES (%s, %s)
    ''', (client_id, phone))

    conn.commit()
    cur.close()
    conn.close()

def update_client(client_id, first_name=None, last_name=None, email=None):
    conn = get_db_connection()
    cur = conn.cursor()

    if first_name:
        cur.execute('''
        UPDATE clients 
        SET first_name = %s 
        WHERE id = %s
        ''', (first_name, client_id))
    
    if last_name:
        cur.execute('''
        UPDATE clients 
        SET last_name = %s 
        WHERE id = %s
        ''', (last_name, client_id))
    
    if email:
        cur.execute('''
        UPDATE clients 
        SET email = %s 
        WHERE id = %s
        ''', (email, client_id))

    conn.commit()
    cur.close()
    conn.close()

def delete_phone(client_id, phone):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
    DELETE FROM phones 
    WHERE client_id = %s AND phone = %s
    ''', (client_id, phone))

    conn.commit()
    cur.close()
    conn.close()

def delete_client(client_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
    DELETE FROM clients 
    WHERE id = %s
    ''', (client_id,))

    conn.commit()
    cur.close()
    conn.close()

def find_client(first_name=None, last_name=None, email=None, phone=None):
    conn = get_db_connection()
    cur = conn.cursor()

    query = '''
    SELECT c.id, c.first_name, c.last_name, c.email, p.phone 
    FROM clients AS c 
    LEFT JOIN phones AS p ON c.id = p.client_id 
    WHERE TRUE
    '''
    params = []

    if first_name:
        query += ' AND c.first_name = %s'
        params.append(first_name)
    if last_name:
        query += ' AND c.last_name = %s'
        params.append(last_name)
    if email:
        query += ' AND c.email = %s'
        params.append(email)
    if phone:
        query += ' AND p.phone = %s'
        params.append(phone)

    cur.execute(query, params)
    clients = cur.fetchall()

    cur.close()
    conn.close()

    return clients


if __name__ == "__main__":
    
    create_database()

    add_client('Михаил', 'Галустян', 'gadya2025@gmail.com')

    clients = find_client(email='gadya2025@gmail.com')
    print("Найденный клиент:", clients)

    add_phone(1, '+7-223-457-2223')
    add_phone(1, '+7-332-754-3222')

    update_client(1, first_name='Михаил', last_name='Пашинян')

    delete_phone(1, '+7-223-457-2223')

    delete_client(1)

    clients = find_client(last_name='Пашинян')
    print("Ищем клиентов по фамилии:", clients)
