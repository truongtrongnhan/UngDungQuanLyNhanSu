from data.init_data import InitData
import configparser

class EmployeeService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./utils/config.ini')
        self.db = InitData(config)
        
    def insert(self, input):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        INSERT INTO employees (
            name, 
            date_of_birth,
            gender, 
            address, 
            phone_number, 
            email,
            position_id,
            start_date,
            id_card_number,
            password,
            username
        )
        VALUES 
        (
            N'{input["name"]}', 
            '{input["date_of_birth"]}',
            {input["gender"]},
            N'{input["address"]}',
            '{input["phone_number"]}',
            '{input["email"]}',
            {input["position_id"]},
            '{input["start_date"]}',
            '{input["id_card_number"]}',
            {'"1"'},
            '{input["username"]}'
        )
        ''')

        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def search(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('''
            SELECT A.employee_id, A.name, A.phone_number, 
            CASE A.gender
                WHEN 0 THEN 'Nữ'
                WHEN 1 THEN 'Nam'
                ELSE 'Unknown'
            END genderName,
            B.position_name,
            DATE_FORMAT(A.start_date, '%d/%m/%Y') AS start_date
            FROM employees A
            LEFT JOIN positions B ON A.position_id = B.position_id
        ''')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    def update(self, data):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        UPDATE employees 
        SET name = N'{data["name"]}', 
        date_of_birth = '{data["date_of_birth"]}', 
        gender = {data["gender"]} , 
        address = N'{data["address"]}',
        phone_number = '{data["phone_number"]}', 
        email = '{data["email"]}', 
        position_id = {data["position_id"]}, 
        start_date = '{data["start_date"]}', 
        id_card_number = {data["id_card_number"]},
        username = '{data["username"]}'
        WHERE employee_id = {data["employee_id"]}
        ''')
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def delete(self, id):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'DELETE FROM employees WHERE employee_id = {id}')
        self.db.connection.commit()
        cursor.close()

        self.db.close_connection()
    def getById(self, id):
        self.db.connect_database()
        cursor = self.db.connection.cursor()

        cursor.execute(f'''
        SELECT employee_id, name, date_of_birth, gender, address, phone_number, email, position_id, start_date, id_card_number, username
        FROM employees                        
        WHERE employee_id = {id}
        ''')

        columns_name = [desc[0] for desc in cursor.description]

        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()

        row_dict = dict(zip(columns_name, row))
        return row_dict
    
    def changePassword(self, id, passwordNew):
        self.db.connect_database()

        cursor = self.db.connection.cursor()
        self.db.connection.cursor().execute(f'''
        UPDATE employees SET password = '{passwordNew}' WHERE employee_id = {id}
        ''')
        self.db.connection.commit()

        cursor.close()
        self.db.close_connection()

    def getCombox(self):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute('''
            SELECT employee_id, name
            FROM employees 
        ''')
        rows = cursor.fetchall()

        cursor.close()
        self.db.close_connection()

        return rows
    
    def getLoginUser(self, username, password):
        self.db.connect_database()
        cursor = self.db.connection.cursor()
        
        cursor.execute(f'''
            SELECT A.name, C.role_id, C.role_name
            FROM employees A
            LEFT JOIN employee_roles B ON A.employee_id = B.employee_id
            LEFT JOIN roles C ON B.role_id = C.role_id
            WHERE A.username = '{username}' AND A.password = '{password}'
        ''')
        row = cursor.fetchone()

        cursor.close()
        self.db.close_connection()

        return row
