import sqlite3
import random

DB_NAME = "students.db"

# Sample Data
first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan", "Diya", "Saanvi", "Ananya", "Aadhya", "Pari", "Anika", "Navya", "Angel", "Myra", "Sara"]
last_names = ["Sharma", "Verma", "Gupta", "Malhotra", "Bhatia", "Mehta", "Joshi", "Nair", "Reddy", "Singh", "Patel", "Chopra", "Desai", "Rao", "Kumar", "Iyer", "Kaur", "Jain", "Saxena", "Tiwari"]
departments = ["Computer Science", "Information Technology", "Electronics & Comm", "Mechanical", "Civil"]

def generate_roll_no(year, dept, index):
    # Format: YYYY-DEPT-XXX (e.g., 2023-CS-001)
    dept_codes = {
        "Computer Science": "CS",
        "Information Technology": "IT",
        "Electronics & Comm": "ECE",
        "Mechanical": "MECH",
        "Civil": "CIVIL"
    }
    academic_year = 2026 - year # year 1 = 2025 batch (approx)
    return f"{academic_year}-{dept_codes[dept]}-{index:03d}"

def populate_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if we already have a lot of data
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    if count > 5:
        print(f"Database already has {count} students. Skipping population.")
        conn.close()
        return

    print("Populating database with sample data...")
    
    students_to_add = []
    generated_rolls = set()

    for _ in range(25):
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first} {last}"
        
        dept = random.choice(departments)
        year = random.randint(1, 4)
        
        # Ensure unique roll no
        index = 1
        while True:
            roll_no = generate_roll_no(year, dept, index)
            if roll_no not in generated_rolls:
                generated_rolls.add(roll_no)
                break
            index += 1
            
        students_to_add.append((name, roll_no, dept, year))

    try:
        cursor.executemany("INSERT INTO students (name, roll_no, department, year) VALUES (?, ?, ?, ?)", students_to_add)
        conn.commit()
        print(f"Successfully added {len(students_to_add)} students.")
    except sqlite3.IntegrityError as e:
        print(f"Error adding data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    populate_db()
