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
        WHERE t.current_tenant = 'True'
        ORDER BY t.tenant_id DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()
    return results


def get_room_numbers():
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT room_number FROM rooms"
    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()
    return [item[0] for item in results]


def insert_house(cursor, house_number):
    cursor.execute("SELECT house_id FROM Houses WHERE house_number=%s", (house_number,))
    house = cursor.fetchone()

    if not house:
        cursor.execute("INSERT INTO Houses (house_number) VALUES (%s)", (house_number,))
        return cursor.lastrowid
    else:
        return house[0]


def insert_cts(cursor, house_id, cts_number):
    cursor.execute("SELECT cts_id FROM CTS WHERE house_id = %s AND cts_number = %s", (house_id, cts_number))
    cts = cursor.fetchone()

    if not cts:
        cursor.execute("INSERT INTO CTS (cts_number, house_id) VALUES (%s, %s)", (cts_number, house_id))
        return cursor.lastrowid
    else:
        return cts[0]


def insert_room(cursor, house_id, cts_id, room_number):
    cursor.execute("SELECT room_id FROM Rooms WHERE room_number=%s AND cts_id=%s AND house_id=%s",
                   (room_number, cts_id, house_id))
    room = cursor.fetchone()

    if not room:
        cursor.execute("INSERT INTO Rooms (room_number, cts_id, house_id) VALUES (%s, %s, %s)",
                       (room_number, cts_id, house_id))
        return cursor.lastrowid
    else:
        return None


def insert_tenant(cursor, tenant_name, tenant_mobile, tenant_dod, tenant_gender, notes, room_id):
    cursor.execute("""
        INSERT INTO Tenants (tenant_name, tenant_mobile, tenant_dod, tenant_gender, notes, room_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (tenant_name, tenant_mobile, tenant_dod, tenant_gender, notes, room_id))


def insert_master_entry(house_number, cts_number, room_number, tenant_name, tenant_mobile, tenant_dod, notes,
                        tenant_gender):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        house_id = insert_house(cursor, house_number)
        cts_id = insert_cts(cursor, house_id, cts_number)
        room_id = insert_room(cursor, house_id, cts_id, room_number)
        if room_id is None:
            return False, "Room already exists for this house and CTS."
        insert_tenant(cursor, tenant_name, tenant_mobile, tenant_dod, tenant_gender, notes, room_id)
        connection.commit()
        return True, "Success"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
        return False, f"Unable to insert data due to {err}"
    finally:
        cursor.close()
        connection.close()


def get_house_id_by_house_number(cursor, house_number):
    return get_id_from_table(cursor, "Houses", {"house_number": house_number})


def get_cts_id_by_cts_number_house_id(cursor, cts_number, house_id):
    return get_id_from_table(cursor, "CTS", {"cts_number": cts_number, "house_id": house_id})


def get_room_id_by_room_number_cts_id_house_id(cursor, room_number, cts_id, house_id):
    return get_id_from_table(cursor, "Rooms", {"room_number": room_number, "cts_id": cts_id, "house_id": house_id})


def get_id_from_table(cursor, table_name, conditions):
    id_column = f"{table_name[:-1].lower()}_id" if table_name.endswith("s") else f"{table_name.lower()}_id"
    query = f"SELECT {id_column} FROM {table_name} WHERE " + " AND ".join([f"{col}=%s" for col in conditions.keys()])
    cursor.execute(query, list(conditions.values()))
    result = cursor.fetchone()
    return result[0] if result else None


def update_tenant_info(cursor, tenant_data, room_id):
    query = """
        UPDATE Tenants
        SET 
            tenant_name = %s,
            tenant_mobile = %s,
            tenant_dod = %s,
            tenant_gender = %s,
            notes = %s
        WHERE current_tenant = %s
        AND room_id = %s
    """
    cursor.execute(query, list(tenant_data.values()) + [room_id])


def insert_into_table(cursor, table_name, data):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(query, list(data.values()))
    return cursor.lastrowid


def update_master_entry(old_house_number, old_cts_number, old_room_number, house_number, cts_number, room_number,
                        tenant_name, tenant_mobile, tenant_dod, notes, tenant_gender):
    connection = create_connection()
    cursor = connection.cursor(buffered=True)

    try:
        # --------------------------------- IF TENANT DETAILS IS UPDATED --------------------------------- #
        if old_house_number == house_number and old_cts_number == cts_number and old_room_number == room_number:
            try:
                old_house_id = get_house_id_by_house_number(cursor, old_house_number)
                old_cts_id = get_cts_id_by_cts_number_house_id(cursor, old_cts_number, old_house_id)
                old_room_id = get_room_id_by_room_number_cts_id_house_id(cursor, old_room_number, old_cts_id,
                                                                         old_house_id)

                tenant_data = {
                    "tenant_name": tenant_name or None,
                    "tenant_mobile": tenant_mobile or None,
                    "tenant_dod": tenant_dod,
                    "tenant_gender": tenant_gender or None,
                    "notes": notes or None,
                    "current_tenant": "True"
                }

                update_tenant_info(cursor, tenant_data, old_room_id)

                connection.commit()
                connection.close()

                return True, "Data Updated Successfully!"
            except Exception as e:
                print(e)

        # --------------------------------- IF HOUSE NUMBER IS UPDATED --------------------------------- #
        if old_house_number != house_number and old_cts_number == cts_number and old_room_number == room_number:
            house_id = get_house_id_by_house_number(cursor, house_number)

            if house_id is None:
                new_house_id = insert_into_table(cursor, "Houses", {"house_number": house_number})
                new_cts_id = insert_into_table(cursor, "CTS", {"cts_number": cts_number, "house_id": new_house_id})

                old_house_id = get_house_id_by_house_number(cursor, old_house_number)
                old_cts_id = get_cts_id_by_cts_number_house_id(cursor, old_cts_number, old_house_id)
                old_room_id = get_room_id_by_room_number_cts_id_house_id(cursor, old_room_number, old_cts_id,
                                                                         old_house_id)

                cursor.execute("UPDATE Rooms SET cts_id=%s, house_id=%s WHERE room_id=%s",
                               (new_cts_id, new_house_id, old_room_id))

                tenant_data = {
                    "tenant_name": tenant_name or None,
                    "tenant_mobile": tenant_mobile or None,
                    "tenant_dod": tenant_dod,
                    "tenant_gender": tenant_gender or None,
                    "notes": notes or None,
                    "current_tenant": "True"
                }

                update_tenant_info(cursor, tenant_data, old_room_id)

                connection.commit()
                connection.close()

                return True, "Data Updated Successfully!"
            else:
                cts_id = get_cts_id_by_cts_number_house_id(cursor, cts_number, house_id)

                if cts_id is None:
                    new_cts_id = insert_into_table(cursor, "CTS", {"cts_number": cts_number, "house_id": house_id})
                    old_cts_id = get_cts_id_by_cts_number_house_id(cursor, old_cts_number, house_id)
                    old_room_id = get_room_id_by_room_number_cts_id_house_id(cursor, old_room_number, old_cts_id,
                                                                             house_id)

                    cursor.execute("UPDATE Rooms SET cts_id=%s, house_id=%s WHERE room_id=%s",
                                   (new_cts_id, house_id, old_room_id))

                    tenant_data = {
                        "tenant_name": tenant_name or None,
                        "tenant_mobile": tenant_mobile or None,
                        "tenant_dod": tenant_dod,
                        "tenant_gender": tenant_gender or None,
                        "notes": notes or None,
                        "current_tenant": "True"
                    }

                    update_tenant_info(cursor, tenant_data, old_room_id)

                    connection.commit()
                    connection.close()
                    return True, "Data Updated Successfully!"

                else:
                    room_id = get_room_id_by_room_number_cts_id_house_id(cursor, room_number, cts_id, house_id)
                    if room_id is None:
                        old_house_id = get_house_id_by_house_number(cursor, old_house_number)
                        old_cts_id = get_cts_id_by_cts_number_house_id(cursor, old_cts_number, old_house_id)
                        old_room_id = get_room_id_by_room_number_cts_id_house_id(cursor, old_room_number,
                                                                                 old_cts_id,
                                                                                 old_house_id)

                        cursor.execute("UPDATE Rooms SET cts_id=%s, house_id=%s WHERE room_id=%s",
                                       (cts_id, house_id, old_room_id))

                        tenant_data = {
                            "tenant_name": tenant_name or None,
                            "tenant_mobile": tenant_mobile or None,
                            "tenant_dod": tenant_dod,
                            "tenant_gender": tenant_gender or None,
                            "notes": notes or None,
                            "current_tenant": "True"
                        }

                        update_tenant_info(cursor, tenant_data, old_room_id)

                        connection.commit()
                        connection.close()

                        return True, "Data Updated Successfully!"
                    else:
                        return False, "Room Number already exists!"

        # --------------------------------- IF CTS NUMBER IS UPDATED --------------------------------- #
        if old_house_number == house_number and old_cts_number != cts_number and old_room_number == room_number:
            old_house_id = get_house_id_by_house_number(cursor, old_house_number)
            cts_id = get_cts_id_by_cts_number_house_id(cursor, cts_number, old_house_id)

            if cts_id is None:
                new_cts_id = insert_into_table(cursor, "CTS", {"cts_number": cts_number, "house_id": old_house_id})
                old_cts_id = get_cts_id_by_cts_number_house_id(cursor, old_cts_number, old_house_id)
                old_room_id = get_room_id_by_room_number_cts_id_house_id(cursor, old_room_number, old_cts_id,
                                                                         old_house_id)

                cursor.execute("UPDATE Rooms SET cts_id=%s WHERE room_id=%s", (new_cts_id, old_room_id))

                tenant_data = {
                    "tenant_name": tenant_name or None,
                    "tenant_mobile": tenant_mobile or None,
                    "tenant_dod": tenant_dod,
                    "tenant_gender": tenant_gender or None,
                    "notes": notes or None,
                    "current_tenant": "True"
                }

                update_tenant_info(cursor, tenant_data, old_room_id)

                connection.commit()
                connection.close()
                return True, "Data Updated Successfully!"

            else:
                room_id = get_room_id_by_room_number_cts_id_house_id(cursor, room_number, cts_id, old_house_id)
                if room_id is None:
                    old_cts_id = get_cts_id_by_cts_number_house_id(cursor, old_cts_number, old_house_id)
                    old_room_id = get_room_id_by_room_number_cts_id_house_id(cursor, old_room_number,
                                                                             old_cts_id,
                                                                             old_house_id)

                    cursor.execute("UPDATE Rooms SET cts_id=%s WHERE room_id=%s",
                                   (cts_id, old_room_id))

                    tenant_data = {
                        "tenant_name": tenant_name or None,
                        "tenant_mobile": tenant_mobile or None,
                        "tenant_dod": tenant_dod,
                        "tenant_gender": tenant_gender or None,
                        "notes": notes or None,
                        "current_tenant": "True"
                    }

                    update_tenant_info(cursor, tenant_data, old_room_id)

                    connection.commit()
                    connection.close()

                    return True, "Data Updated Successfully!"
                else:
                    return False, "Room Number already exists!"

        # --------------------------------- IF ROOM NUMBER IS UPDATED --------------------------------- #
        if old_house_number == house_number and old_cts_number == cts_number and old_room_number != room_number:
            old_house_id = get_house_id_by_house_number(cursor, old_house_number)
            old_cts_id = get_cts_id_by_cts_number_house_id(cursor, old_cts_number, old_house_id)
            room_id = get_room_id_by_room_number_cts_id_house_id(cursor, room_number, old_cts_id, old_house_id)
            if room_id is None:
                old_room_id = get_room_id_by_room_number_cts_id_house_id(cursor, old_room_number,
                                                                         old_cts_id,
                                                                         old_house_id)

                cursor.execute("UPDATE Rooms SET room_number=%s WHERE room_id=%s", (room_number, old_room_id))

                tenant_data = {
                    "tenant_name": tenant_name or None,
                    "tenant_mobile": tenant_mobile or None,
                    "tenant_dod": tenant_dod,
                    "tenant_gender": tenant_gender or None,
                    "notes": notes or None,
                    "current_tenant": "True"
                }

                update_tenant_info(cursor, tenant_data, old_room_id)

                connection.commit()
                connection.close()

                return True, "Data Updated Successfully!"
            else:
                return False, "Room Number already exists!"

    except:
        connection.rollback()
        return False, "Unable to Update Data!"
    finally:
        cursor.close()
        connection.close()


def delete_master_entry(old_house_number, old_cts_number, old_room_number):
    connection = create_connection()
    cursor = connection.cursor()

    house_id_query = "SELECT house_id FROM Houses WHERE house_number = %s"
    cursor.execute(house_id_query, (old_house_number,))
    house_id = cursor.fetchone()[0]

    # Fetching the cts_id based on cts_number and house_id
    cts_id_query = "SELECT cts_id FROM CTS WHERE cts_number = %s AND house_id = %s"
    cursor.execute(cts_id_query, (old_cts_number, house_id))
    cts_id = cursor.fetchone()[0]

    # Fetching the room_id based on room_number, cts_id, and house_id
    room_id_query = "SELECT room_id FROM Rooms WHERE room_number = %s AND cts_id = %s AND house_id = %s"
    cursor.execute(room_id_query, (old_room_number, cts_id, house_id))
    room_id = cursor.fetchone()[0]

    # Deleting the tenant based on room_id
    tenant_query = "DELETE FROM Tenants WHERE room_id = %s AND current_tenant = %s"
    cursor.execute(tenant_query, (room_id, 'True'))

    tenant_count_query = "SELECT count(*) FROM Tenants WHERE room_id = %s"
    cursor.execute(tenant_count_query, (room_id,))
    tenant_count = cursor.fetchone()[0]

    if not tenant_count:
        room_query = "DELETE FROM Rooms WHERE room_id = %s"
        cursor.execute(room_query, (room_id,))

    connection.commit()
    cursor.close()
    connection.close()


def get_house_data():
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT house_number, house_id FROM Houses"
    cursor.execute(query)
    results = cursor.fetchall()

    connection.close()
    return [[item[0], item[1]] for item in results]


def get_rooms_data_by_house_id(house_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT room_number, room_id FROM Rooms WHERE house_id=%s"
    cursor.execute(query, (house_id,))
    results = cursor.fetchall()

    connection.close()
    return [[item[0], item[1]] for item in results]


def get_cts_number_by_room_id(room_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT cts_id FROM Rooms WHERE room_id=%s"
    cursor.execute(query, (room_id,))
    cts_id = cursor.fetchone()[0]

    query = "SELECT DISTINCT cts_number FROM CTS WHERE cts_id=%s"
    cursor.execute(query, (cts_id,))
    cts_number = cursor.fetchone()[0]

    connection.close()
    return cts_number
