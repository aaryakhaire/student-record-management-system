from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

DB_NAME = "students.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        department = request.form['department']
        year = request.form['year']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO students (name, roll_no, department, year) VALUES (?, ?, ?, ?)",
                           (name, roll_no, department, year))
            conn.commit()
            flash("Student added successfully!", "success")
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash(f"Error: Roll Number '{roll_no}' already exists.", "error")
        finally:
            conn.close()

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        department = request.form['department']
        year = request.form['year']

        try:
            cursor.execute("UPDATE students SET name=?, roll_no=?, department=?, year=? WHERE id=?",
                           (name, roll_no, department, year, id))
            conn.commit()
            flash("Student updated successfully!", "success")
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash(f"Error: Roll Number '{roll_no}' already exists.", "error")
        finally:
            conn.close()

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()
    
    if student:
        return render_template('edit.html', student=student)
    else:
        flash("Student not found.", "error")
        return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Student deleted successfully!", "success")
    return redirect(url_for('index'))

@app.route('/reports')
def reports():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Students by Department
    cursor.execute("SELECT department, COUNT(*) FROM students GROUP BY department")
    dept_data = cursor.fetchall()
    dept_labels = [row[0] for row in dept_data]
    dept_counts = [row[1] for row in dept_data]

    # Students by Year
    cursor.execute("SELECT year, COUNT(*) FROM students GROUP BY year")
    year_data = cursor.fetchall()
    year_labels = [f"Year {row[0]}" for row in year_data]
    year_counts = [row[1] for row in year_data]
    
    # Total Students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    conn.close()
    
    return render_template('reports.html', 
                           dept_labels=dept_labels, dept_counts=dept_counts,
                           year_labels=year_labels, year_counts=year_counts,
                           total_students=total_students)

if __name__ == '__main__':
    app.run(debug=True)
