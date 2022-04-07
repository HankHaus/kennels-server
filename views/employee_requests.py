EMPLOYEES = [
        {
            "id": 1,
            "name": "Willy Wonka",
            "locationId": "1"
        },
        {
            "id": 2,
            "name": "Ty Dolla Sign",
            "locationId": "2"
        }
    ]


def get_single_employee(id):
    """_summary_

    Args:
        id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Variable to hold the found animal, if it exists
    requested_employee = None

    # Iterate the ANIMALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for employee in     EMPLOYEES:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if employee["id"] == id:
            requested_employee = employee

    return requested_employee


def get_all_employees():
    """_summary_

    Returns:
        _type_: _description_
    """
    return EMPLOYEES

def create_employee(employee):
    """_summary_

    Args:
        animal (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Get the id value of the last animal in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    employee["id"] = new_id

    # Add the animal dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee
