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
        ORDER BY h.house_number ASC, r.room_number ASC, t.tenant_id DESC
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


def insert_tenant(cursor, tenant_name, tenant_mobile, tenant_dod, tenant_gender, notes, current_tenant, room_id):
    cursor.execute("""
        INSERT INTO Tenants (tenant_name, tenant_mobile, tenant_dod, tenant_gender, notes, current_tenant, room_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (tenant_name, tenant_mobile, tenant_dod, tenant_gender, notes, current_tenant, room_id))


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
        current_tenant = "True"
        insert_tenant(cursor, tenant_name, tenant_mobile, tenant_dod, tenant_gender, notes, current_tenant, room_id)
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


def get_tenant_id_by_room_id(cursor, room_id, current_tenant):
    return get_id_from_table(cursor, "Tenants", {"room_id": room_id, "current_tenant": current_tenant})


def get_tenant_id_by_bill_id(cursor, bill_id):
    return get_id_from_table(cursor, "Bills", {"bill_id": bill_id})


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


def get_latest_book_and_bill_numbers():
    connection = create_connection()
    cursor = connection.cursor()

    # Query to get the maximum bill_number for the maximum book_number
    query = """
    SELECT
        book_number,
        MAX(bill_number) AS max_bill_number
    FROM 
        Bill
    WHERE 
        book_number = (SELECT MAX(book_number) FROM Bill)
    """

    cursor.execute(query)
    result = cursor.fetchone()
    connection.close()

    # Make sure to check that result is not None in case the table is empty
    if result is None:
        return 1, 1  # Assuming 0 as a starting point if there are no entries

    max_book_number, max_bill_number = result
    return max_book_number, max_bill_number


def get_last_from_and_to_dates(house_number, room_number, cts_number, operation):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        current_tenant = "True"
        house_id = get_house_id_by_house_number(cursor, house_number)
        cts_id = get_cts_id_by_cts_number_house_id(cursor, cts_number, house_id)
        room_id = get_room_id_by_room_number_cts_id_house_id(cursor, room_number, cts_id, house_id)
        tenant_id = get_tenant_id_by_room_id(cursor, room_id, current_tenant)

        if operation == 'insert':
            subquery = "(SELECT MAX(bill_id) FROM bills WHERE tenant_id = %s)"
        elif operation == 'update':
            subquery = "(SELECT bill_id FROM bills WHERE tenant_id = %s ORDER BY bill_id DESC LIMIT 1 OFFSET 1)"
        else:
            raise ValueError("Invalid operation type")

        query = (
            "SELECT rent_from, rent_to "
            "FROM bills "
            "WHERE tenant_id = %s "
            f"AND bill_id = {subquery}"
        )
        cursor.execute(query, (tenant_id, tenant_id))
        result = cursor.fetchall()
        connection.close()

        if not result:
            return None, None

        previous_rent_from_date, previous_rent_to_date = result[0]

        return previous_rent_from_date, previous_rent_to_date

    except mysql.connector.Error as err:
        print(str(err))
        return None, None


def get_adjacent_from_and_to_dates(house_number, room_number, cts_number):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        current_tenant = "True"
        house_id = get_house_id_by_house_number(cursor, house_number)
        cts_id = get_cts_id_by_cts_number_house_id(cursor, cts_number, house_id)
        room_id = get_room_id_by_room_number_cts_id_house_id(cursor, room_number, cts_id, house_id)
        tenant_id = get_tenant_id_by_room_id(cursor, room_id, current_tenant)

        subquery_previous = "(SELECT MAX(bill_id) FROM bills WHERE tenant_id = %s AND bill_id < %s)"
        subquery_next = "(SELECT MIN(bill_id) FROM bills WHERE tenant_id = %s AND bill_id > %s)"

        query = (
            "SELECT rent_from, rent_to "
            "FROM bills "
            "WHERE tenant_id = %s "
            f"AND bill_id IN ({subquery_previous}, %s, {subquery_next})"
        )

        print(query)

        cursor.execute(query, (tenant_id, tenant_id, tenant_id))
        result = cursor.fetchall()
        connection.close()

        for res in result:
            print(res)
        if not result or len(result) != 3:
            return None, None, None

        previous_rent_from_date, previous_rent_to_date = result[0]
        current_rent_from_date, current_rent_to_date = result[1]
        next_rent_from_date, next_rent_to_date = result[2]

        return previous_rent_from_date, previous_rent_to_date, next_rent_from_date, next_rent_to_date

    except mysql.connector.Error as err:
        print(str(err))
        return None, None, None, None


def insert_bill_entry(rent_month, book_number, bill_number, purpose_for, rent_from, rent_to, at_the_rate_of,
                      total_months, total_rupees, received_date, extra_payment, agreement_date, notes,
                      tenant_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        insert_query = """
            INSERT INTO BILLS (bill_for_month_of, book_number, bill_number, purpose_for, rent_from, rent_to,
            at_the_rate_of, total_months, total_rupees, received_date, extra_payment, agreement_date, notes, tenant_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (rent_month, book_number, bill_number,
                                      purpose_for, rent_from, rent_to, at_the_rate_of,
                                      total_months, total_rupees, received_date, extra_payment,
                                      agreement_date, notes, tenant_id))

        connection.commit()
        return True, "Success"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
        return False, f"Unable to insert data due to {err}"
    finally:
        cursor.close()
        connection.close()


def update_bill_entry(bill_id, rent_month, book_number, bill_number, purpose_for,
                      rent_from, rent_to, at_the_rate_of, total_months, total_rupees,
                      received_date, extra_payment, agreement_date, notes):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        update_query = """
            UPDATE bills 
            SET bill_for_month_of = %s, 
                book_number = %s, 
                bill_number = %s, 
                purpose_for = %s, 
                rent_from = %s, 
                rent_to = %s, 
                at_the_rate_of = %s, 
                total_months = %s, 
                total_rupees = %s, 
                received_date = %s, 
                extra_payment = %s, 
                agreement_date = %s, 
                notes = %s 
            WHERE bill_id = %s
        """
        cursor.execute(update_query, (rent_month, book_number, bill_number,
                                      purpose_for, rent_from, rent_to, at_the_rate_of,
                                      total_months, total_rupees, received_date, extra_payment,
                                      agreement_date, notes, bill_id))

        connection.commit()
        return True, "Success"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
        return False, f"Unable to insert data due to {err}"
    finally:
        cursor.close()
        connection.close()


def fetch_data_for_edit_record(bill_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        query = """
            SELECT bill_for_month_of, notes
            FROM bills
            WHERE bill_id = %s
        """
        cursor.execute(query, (bill_id,))
        result = cursor.fetchone()

        connection.close()

        if result:
            return result
        else:
            return None, None

    except mysql.connector.Error as err:
        print("Error:", str(err))
        return None, None


def get_bill_table_data():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
            SELECT
            b.received_date AS "Received Date",
            h.house_number AS "House No.",
            r.room_number AS "Room No.",
            c.cts_number AS "CTS No.",
            t.tenant_name AS "Tenant Name",
            b.rent_from AS "Rent From",
            b.rent_to AS "Rent To",
            b.at_the_rate_of AS "@",
            b.total_months AS "Total Month(s)",
            b.total_rupees AS "Total Amount",
            b.book_number AS "Book No.",
            b.bill_number AS "Bill No.",
            b.extra_payment AS "Extra Payment",
            b.purpose_for AS "Purpose For",
            t.tenant_mobile AS "Mobile",
            t.tenant_dod AS "DoD",
            b.agreement_date AS "Agreement Date",
            b.notes AS "Notes",
            t.tenant_gender AS "Gender",
            b.bill_id AS "Bill ID"
        FROM
            bills b
        JOIN
            tenants t ON b.tenant_id = t.tenant_id
        JOIN
            rooms r ON t.room_id = r.room_id
        JOIN
            cts c ON r.cts_id = c.cts_id
        JOIN
            houses h ON c.house_id = h.house_id
        ORDER BY
            b.bill_id DESC;
    """
    # h.house_number ASC, r.room_number ASC, b.bill_id DESC;
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    return result


def get_latest_bill_data_by_tenant_id(tenant_id):
    pass


def delete_bill_by_id(bill_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        delete_query = "DELETE FROM bills WHERE bill_id = %s"
        cursor.execute(delete_query, (bill_id,))

        connection.commit()  # Committing the transaction
        print(f"Bill with ID {bill_id} has been deleted.")

        return True, 'Success'

    except mysql.connector.Error as err:
        print("Error:", str(err))
        return False, str(err)

    finally:
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


def get_tenant_name_by_bill_id(bill_id):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        tenant_id_query = "SELECT tenant_id FROM Bills WHERE bill_id = %s"
        cursor.execute(tenant_id_query, (bill_id,))
        tenant_id = cursor.fetchone()[0]
        tenant_name_query = "SELECT tenant_name FROM Tenants WHERE tenant_id = %s"
        cursor.execute(tenant_name_query, (tenant_id,))
        tenant_name = cursor.fetchone()[0]
        connection.close()
        return tenant_name

    except mysql.connector.Error as err:
        print("Error:", str(err))
        return False

    finally:
        cursor.close()
        connection.close()


def get_tenants_data_by_room_id(room_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT tenant_name, tenant_id FROM Tenants WHERE room_id=%s AND current_tenant=%s"
    current_tenant = 'True'
    cursor.execute(query, (room_id, current_tenant))
    results = cursor.fetchone()

    connection.close()
    return results[0], results[1]


def get_room_data_by_tenant_id(tenant_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT room_id FROM Tenants WHERE tenant_id=%s AND current_tenant=%s"
    current_tenant = 'True'
    cursor.execute(query, (tenant_id, current_tenant))
    room_id = cursor.fetchone()[0]

    room_name_query = "SELECT DISTINCT room_number FROM Rooms WHERE room_id=%s"
    cursor.execute(room_name_query, (room_id,))
    room_name = cursor.fetchone()[0]

    connection.close()
    return room_name, room_id


def get_tenant_name_by_tenant_id(tenant_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT tenant_name FROM Tenants WHERE tenant_id=%s AND current_tenant=%s"
    current_tenant = "True"
    cursor.execute(query, (tenant_id, current_tenant))
    tenant_name = cursor.fetchone()[0]

    connection.close()

    return tenant_name
