import sqlite3
import json
from models import Employee
from models import Location
from models import Animal



def get_all_employees():
    """_summary_

    Returns:
        _type_: _description_
    """
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.location_id,
            l.name location_name,
            l.address location_address
        FROM employee e
        JOIN Location l
            ON l.id = e.location_id
        """)

        # Initialize an empty list to hold all animal representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            employee = Employee(row['id'], row['name'], row['location_id'])

            location = Location(row['location_id'], row['location_name'], row['location_address'])

            employee.location = location.__dict__

            employees.append(employee.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)


def get_single_employee(id):
    """_summary_

    Args:
        id (_type_): _description_

    Returns:
        _type_: _description_
    """
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.location_id,
            l.id location_id,
            l.name location_name,
            l.address location_address,
            a.id animal_id,
            a.name animal_name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM employee e
        JOIN location l
            ON l.id = a.location_id
        JOIN animal a
            ON a.location_id = e.location_id
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()
        location = Location(data['location_id'], data['location_name'], data['location_address'])

        animal = Animal(data['id'], data['animal_name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

        # Create an animal instance from the current row
        employee = Employee(data['id'], data['name'], data['location_id'], location.__dict__, animal.__dict__)

        return json.dumps(employee.__dict__)



def get_employees_by_location(location_id):
    """_summary_

    Args:
        email (_type_): _description_

    Returns:
        _type_: _description_
    """

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            e.id,
            e.name,
            e.location_id
        from Employee e
        WHERE e.location_id = ?
        """, ( location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['location_id'])
            employees.append(employee.__dict__)

    return json.dumps(employees)
