import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="societydb"
    )


def check_credentials(username, password):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchall()

    connection.close()
    return len(result) > 0


def get_house_numbers():
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT house_number FROM Houses"
    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()
    return [item[0] for item in results]

def get_cts_numbers():
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT cts_number FROM cts"
    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()
    return [item[0] for item in results]

def get_room_numbers():
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT room_number FROM rooms"
    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()
    return [item[0] for item in results]


def insert_master_entry(house_number, cts_number, room_number, tenant_name, tenant_mobile, tenant_dod, notes, tenant_gender):
    connection = create_connection()
    cursor = connection.cursor()

    # Step 1: Handle House Number
    cursor.execute("SELECT house_id FROM Houses WHERE house_number=%s", (house_number,))
    house = cursor.fetchone()

    if not house:
        cursor.execute("INSERT INTO Houses (house_number) VALUES (%s)", (house_number,))
        house_id = cursor.lastrowid
    else:
        house_id = house[0]

    # Step 2: Handle CTS Number
    cursor.execute("SELECT cts_id FROM CTS WHERE cts_number=%s", (cts_number,))
    cts = cursor.fetchone()

    if not cts:
        cursor.execute("INSERT INTO CTS (cts_number, house_id) VALUES (%s, %s)", (cts_number, house_id))
        cts_id = cursor.lastrowid
    else:
        cts_id = cts[0]

    # Step 3: Handle Room Number
    cursor.execute("SELECT room_id FROM Rooms WHERE room_number=%s AND cts_id=%s", (room_number, cts_id))
    room = cursor.fetchone()

    if not room:
        cursor.execute("INSERT INTO Rooms (room_number, cts_id, house_id) VALUES (%s, %s, %s)", (room_number, cts_id, house_id))
        room_id = cursor.lastrowid
    else:
        room_id = room[0]

    # Step 4: Insert Tenant Details
    cursor.execute("""
        INSERT INTO Tenants (tenant_name, tenant_mobile, tenant_dod, tenant_gender, notes, room_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (tenant_name, tenant_mobile, tenant_dod, tenant_gender, notes, room_id))

    connection.commit()
    connection.close()


def get_all_master_entries():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)  # Use dictionary=True to fetch results as dictionaries

    query = """
        SELECT
            h.house_number,
            c.cts_number,
            r.room_number,
            t.tenant_name,
            t.tenant_mobile,
            t.tenant_dod,
            t.notes,
            t.tenant_gender
        FROM Tenants t
        JOIN Rooms r ON t.room_id = r.room_id
        JOIN CTS c ON r.cts_id = c.cts_id
        JOIN Houses h ON c.house_id = h.house_id
    """
    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()
    return results


def update_master_entry(old_house_number, old_cts_number, old_room_number, house_number, cts_number, room_number, tenant_name, tenant_mobile, tenant_dod, notes, tenant_gender):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Fetch house_id using old_house_number
        cursor.execute("SELECT house_id FROM Houses WHERE house_number = %s", (old_house_number,))
        house_id = cursor.fetchone()[0]
        print(old_house_number, house_id)

        # Fetch cts_id using old_cts_number and house_id
        cursor.execute("SELECT cts_id FROM CTS WHERE cts_number = %s AND house_id = %s", (old_cts_number, house_id))
        cts_id = cursor.fetchone()[0]
        print(old_cts_number, cts_id)

        # Fetch room_id using old_room_number, cts_id, and house_id
        cursor.execute("SELECT room_id FROM Rooms WHERE room_number = %s AND cts_id = %s AND house_id = %s", (old_room_number, cts_id, house_id))
        room_id = cursor.fetchone()[0]
        print(old_room_number, room_id)

        # Update Houses, CTS, Rooms, and Tenants tables
        try:
            cursor.execute("UPDATE Houses SET house_number = %s WHERE house_id = %s", (house_number, house_id))
            cursor.execute("UPDATE CTS SET cts_number = %s WHERE cts_id = %s", (cts_number, cts_id))
            cursor.execute("UPDATE Rooms SET room_number = %s WHERE room_id = %s", (room_number, room_id))
        except Exception as e:
            print(e, 'Error updating HOUSE, CTS, Room')

        try:
            cursor.execute("""
                UPDATE Tenants 
                SET tenant_name = %s, tenant_mobile = %s, tenant_dod = %s, tenant_gender = %s, notes = %s 
                WHERE room_id = %s
                """, (tenant_name, tenant_mobile, tenant_dod, tenant_gender, notes, room_id))
        except Exception as e:
            print(e, 'Error updating tenants')

        print()
        connection.commit()
        connection.close()

    except Exception as e:
        print(old_house_number, old_cts_number, old_room_number, house_number, cts_number, room_number, tenant_name, tenant_mobile, tenant_dod, notes, tenant_gender)
        print(f"An error occurred: {e}")
        connection.rollback()
    finally:
        connection.close()

def delete_master_entry(old_house_number, old_cts_number, old_room_number):
    connection = create_connection()
    cursor = connection.cursor()

    house_query = "SELECT house_id FROM Houses WHERE house_number = %s"
    print(house_query)
    cursor.execute(house_query, (old_house_number,))
    house_id = cursor.fetchone()[0]

    # Fetching the cts_id based on cts_number and house_id
    cts_query = "SELECT cts_id FROM CTS WHERE cts_number = %s AND house_id = %s"
    print(cts_query)
    cursor.execute(cts_query, (old_cts_number, house_id))
    cts_id = cursor.fetchone()[0]

    # Fetching the room_id based on room_number, cts_id, and house_id
    room_query = "SELECT room_id FROM Rooms WHERE room_number = %s AND cts_id = %s AND house_id = %s"
    print(room_query)
    cursor.execute(room_query, (old_room_number, cts_id, house_id))
    room_id = cursor.fetchone()[0]

    print(house_id, cts_id, room_id)
    # Deleting the tenant based on room_id
    tenant_query = "DELETE FROM Tenants WHERE room_id = %s"
    cursor.execute(tenant_query, (room_id,))

    connection.commit()
    cursor.close()
    connection.close()

