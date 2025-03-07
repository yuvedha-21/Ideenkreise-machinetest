def top_employees_by_department(employees, department, N):
    filtered_employees = []
    for emp in employees:
        if emp["department"] == department:
            filtered_employees.append(emp)

    sorted_employees = sorted(filtered_employees, key=lambda x: x["salary"], reverse=True)

    return sorted_employees[:N]

employees = [
    {"id": 1, "name": "A", "department": "IT", "salary": 70000},
    {"id": 2, "name": "B", "department": "HR", "salary": 50000},
    {"id": 3, "name": "C", "department": "IT", "salary": 90000},
    {"id": 4, "name": "D", "department": "HR", "salary": 60000},
    {"id": 5, "name": "E", "department": "IT", "salary": 80000},
]

top_it_employees = top_employees_by_department(employees, "IT", 2)

for emp in top_it_employees:
    print(f"ID: {emp['id']}, Name: {emp['name']}, Salary: {emp['salary']}")


