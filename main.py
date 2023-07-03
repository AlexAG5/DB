import psycopg2


def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id SERIAL  PRIMARY KEY, 
        first_name VARCHAR(60) NOT NULL,
        last_name  VARCHAR(60) NOT NULL,
        email      VARCHAR(60) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL    PRIMARY KEY,
        phone_number BIGINT,
        client_id    INTEGER NOT NULL REFERENCES clients(id)
    );
    """)
    print("Таблицы успешно созданы")


def add_client(cur, first_name: str, last_name: str, email, phone_number):
    if phone_number == "":
        phone_number = None
    cur.execute("""
    INSERT INTO clients (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id;
    """, (first_name, last_name, email))
    client_id = cur.fetchone()[0]

    cur.execute("""
    INSERT INTO phones (phone_number, client_id) VALUES (%s, %s) RETURNING id;
    """, (phone_number, client_id))

    cur.execute("""
    SELECT * FROM clients;
    """)
    print(cur.fetchall())

    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())


def add_phone(cur, phone_number, client_id):
    cur.execute("""
    INSERT INTO phones (phone_number, client_id) VALUES (%s, %s) RETURNING id; 
    """, (phone_number, client_id))
    cur.execute("""
    SELECT * FROM Phones;
    """)
    print(cur.fetchall())


def change_data(cur, client_id, first_name, last_name, email, phone_number):
    cur.execute("""
    UPDATE clients SET first_name=%s WHERE id=%s;
    """, (first_name, client_id))
    cur.execute("""
    SELECT first_name FROM clients WHERE id=%s;
    """, (client_id,))
    print("Имя изменено: ", cur.fetchone())

    cur.execute("""
    UPDATE clients SET last_name=%s WHERE id=%s;
    """, (last_name, client_id))
    cur.execute("""
    SELECT last_name FROM clients WHERE id=%s;
    """, (client_id,))
    print("Фамилия изменена: ", cur.fetchone())

    cur.execute("""
    UPDATE clients SET email=%s WHERE id=%s;
    """, (email, client_id))
    cur.execute("""
    SELECT email FROM clients WHERE id=%s;
    """, (client_id,))
    print("Email изменён: ", cur.fetchone())

    cur.execute("""
    UPDATE phones SET phone_number=%s WHERE id=%s;
    """, (phone_number, client_id))
    cur.execute("""
    SELECT phone_number FROM phones WHERE id=%s;
    """, (client_id,))
    print("Телефон изменён: ", cur.fetchone())


def delete_phone(cur, client_id, phone_number):
    cur.execute("""
    DELETE FROM public.phones WHERE client_id=%s AND phone_number=%s;
    """, (client_id, phone_number))
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())


def delete_client(cur, client_id):

    cur.execute(""" 
    DELETE FROM phones WHERE id=%s;
    """, (client_id,))

    cur.execute(""" 
    DELETE FROM clients WHERE id=%s;
    """, (client_id,))

    cur.execute("""
    SELECT * FROM clients;
    """)
    print(cur.fetchall())

    cur.execute("""
        SELECT * FROM phones;
        """)
    print(cur.fetchall())


def search_client(cur, first_name, last_name, email, phone_number):
    if first_name == "":
        first_name = None
    if last_name == "":
        last_name = None
    if email == "":
        email = None
    if phone_number == "":
        phone_number = None
    cur.execute("""
    SELECT * FROM clients c
    JOIN phones p ON c.id = p.client_id
    WHERE first_name=%s OR last_name=%s OR email=%s OR phone_number=%s
    """, (first_name, last_name, email, phone_number))
    print(cur.fetchall())


def delete_db(cur):
    cur.execute("""
    DROP TABLE phones;
    DROP TABLE clients;
    """)
    print("Таблицы успешно удалены")


def main():
    print('Используйте команды: ''1 - Создать БД, 2 - Добавить нового клиента,'
          ' 3 - Добавить телефон для существующего клиента,\n 4 - Изменить данные о клиенте,'
          ' 5 - Удалить телефон у существующего клиента,'
          ' 6 - Удалить существующего клиента,\n 7 - Найти клиента по его данным(имени, фамилии, email или телефону),'
          ' 8 - Удалить таблицы, 9 - Завершить ввод и отправить данные')
    with psycopg2.connect(database="clients_db", user="postgres", password="123") as conn:
        with conn.cursor() as cur:
            while True:
                command = input("Введите команду: ")
                if command == "1":
                    create_db(cur)
                    conn.commit()
                if command == "2":
                    add_client(cur, first_name=input("Введите имя "), last_name=input("Введите фамилию "),
                               email=input("Введите email "), phone_number=input("Введите телефон "))
                if command == "3":
                    add_phone(cur, input("Введите телефон "), input("Введите id клиента "))
                if command == "4":
                    change_data(cur, input("Введите id клиента "), first_name=input("Введите имя "),
                                last_name=input("Введите фамилию "), email=input("Введите email "),
                                phone_number=input("Введите телефон "))
                if command == "5":
                    delete_phone(cur, input("Введите id клиента "), input("Введите телефон который надо удалить "))
                if command == "6":
                    delete_client(cur, input("Введите id клиента "))
                if command == "7":
                    search_client(cur, input("Введите имя "), input("Введите фамилию "),
                                  input("Введите email "), input("Введите телефон "))
                if command == "8":
                    delete_db(cur)
                if command == "9":
                    break

    conn.close()


if __name__ == '__main__':
    main()
