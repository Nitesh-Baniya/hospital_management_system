from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hospital_db"
    )

@app.route('/')
def home():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    # Get data for dashboard
    cur.execute("SELECT * FROM patient")
    patients = cur.fetchall()
    
    cur.execute("SELECT d.D_ID, e.First_Name, e.Last_Name, d.Dept FROM doctor d JOIN employee e ON d.D_ID=e.E_ID")
    doctors = cur.fetchall()
    
    cur.execute("SELECT a.*, p.First_Name as Patient_Name FROM appointment a JOIN patient p ON a.P_ID = p.P_ID")
    appts = cur.fetchall()
    
    cur.execute("SELECT b.*, p.First_Name FROM bills b JOIN patient p ON b.P_ID = p.P_ID")
    bills = cur.fetchall()
    
    return render_template('dashboard.html', patients=patients, doctors=doctors, appts=appts, bills=bills)

@app.route('/patients')
def patients():
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    # Handle search functionality
    search_query = request.args.get('q', '')
    if search_query:
        cur.execute("SELECT * FROM patient WHERE First_Name LIKE %s OR Last_Name LIKE %s OR P_ID LIKE %s", 
                   (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
    else:
        cur.execute("SELECT * FROM patient")
    
    return render_template('patients.html', patients=cur.fetchall(), search_query=search_query)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO patient (First_Name, Last_Name, DOB, Gender) VALUES (%s,%s,%s,%s)",
                (request.form['first_name'], request.form['last_name'], request.form['dob'], request.form['gender']))
    db.commit()
    return redirect('/patients')

@app.route('/edit_patient/<int:patient_id>')
def edit_patient(patient_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        cur.execute("UPDATE patient SET First_Name=%s, Last_Name=%s, DOB=%s, Gender=%s WHERE P_ID=%s",
                   (request.form['first_name'], request.form['last_name'], request.form['dob'], request.form['gender'], patient_id))
        db.commit()
        return redirect('/patients')
    else:
        cur.execute("SELECT * FROM patient WHERE P_ID = %s", (patient_id,))
        patient = cur.fetchone()
        return render_template('edit_patient.html', patient=patient)

@app.route('/delete_patient/<int:patient_id>')
def delete_patient(patient_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM patient WHERE P_ID = %s", (patient_id,))
    db.commit()
    return redirect('/patients')

@app.route('/doctors')
def doctors():
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    # Handle search functionality
    search_query = request.args.get('q', '')
    if search_query:
        cur.execute("""SELECT d.D_ID, e.First_Name, e.Last_Name, d.Dept 
                     FROM doctor d JOIN employee e ON d.D_ID=e.E_ID 
                     WHERE e.First_Name LIKE %s OR e.Last_Name LIKE %s OR d.Dept LIKE %s OR d.D_ID LIKE %s""", 
                   (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
    else:
        cur.execute("SELECT d.D_ID, e.First_Name, e.Last_Name, d.Dept FROM doctor d JOIN employee e ON d.D_ID=e.E_ID")
    
    return render_template('doctors.html', doctors=cur.fetchall(), search_query=search_query)

@app.route('/appointments')
def appointments():
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    # Handle search functionality
    search_query = request.args.get('q', '')
    if search_query:
        cur.execute("""SELECT a.*, p.First_Name as Patient_Name 
                     FROM appointment a 
                     JOIN patient p ON a.P_ID = p.P_ID
                     WHERE p.First_Name LIKE %s OR a.Type LIKE %s OR a.A_ID LIKE %s OR a.Appt_Date LIKE %s""", 
                   (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
    else:
        cur.execute("""SELECT a.*, p.First_Name as Patient_Name 
                     FROM appointment a 
                     JOIN patient p ON a.P_ID = p.P_ID""")
    
    return render_template('appointments.html', appts=cur.fetchall(), search_query=search_query)

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO appointment (P_ID, D_ID, Type, Appt_Date, Appt_Time) VALUES (%s,%s,%s,%s,%s)",
                (request.form['p_id'], request.form['d_id'], request.form['type'], request.form['date'], request.form['time']))
    db.commit()
    return redirect('/appointments')

@app.route('/delete_appointment/<int:apt_id>')
def delete_appointment(apt_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM appointment WHERE A_ID = %s", (apt_id,))
    db.commit()
    return redirect('/appointments')

@app.route('/bills')
def bills():
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    # Handle search functionality
    search_query = request.args.get('q', '')
    if search_query:
        cur.execute("""SELECT b.*, p.First_Name 
                     FROM bills b 
                     JOIN patient p ON b.P_ID = p.P_ID
                     WHERE p.First_Name LIKE %s OR b.B_ID LIKE %s OR b.Amount LIKE %s OR b.Bill_Date LIKE %s""", 
                   (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
    else:
        cur.execute("SELECT b.*, p.First_Name FROM bills b JOIN patient p ON b.P_ID = p.P_ID")
    
    return render_template('bills.html', bills=cur.fetchall(), search_query=search_query)

@app.route('/add_bill', methods=['POST'])
def add_bill():
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO bills (P_ID, Amount, Bill_Date) VALUES (%s,%s,%s)",
                (request.form['p_id'], request.form['amount'], request.form['date']))
    db.commit()
    return redirect('/bills')

@app.route('/mark_bill_paid/<int:bill_id>')
def mark_bill_paid(bill_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    # Check if Status column exists
    cur.execute("SHOW COLUMNS FROM bills LIKE 'Status'")
    status_column = cur.fetchone()
    
    if not status_column:
        # Add Status column if it doesn't exist
        cur.execute("ALTER TABLE bills ADD COLUMN Status VARCHAR(20) DEFAULT 'Pending'")
        pass  # Column might already exist
    
    cur.execute("UPDATE bills SET Status = 'Paid' WHERE B_ID = %s", (bill_id,))
    db.commit()
    return redirect('/bills')

@app.route('/delete_bill/<int:bill_id>')
def delete_bill(bill_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM bills WHERE B_ID = %s", (bill_id,))
    db.commit()
    return redirect('/bills')

@app.route('/reports')
def reports():
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    # Handle search functionality
    search_query = request.args.get('q', '')
    if search_query:
        cur.execute("""SELECT r.*, p.First_Name 
                     FROM reports r 
                     JOIN patient p ON r.P_ID = p.P_ID
                     WHERE p.First_Name LIKE %s OR r.R_ID LIKE %s OR r.Test_Type LIKE %s OR r.Result LIKE %s OR r.Report_Date LIKE %s""", 
                   (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
    else:
        cur.execute("SELECT r.*, p.First_Name FROM reports r JOIN patient p ON r.P_ID = p.P_ID")
    
    return render_template('reports.html', reports=cur.fetchall(), search_query=search_query)

@app.route('/add_report', methods=['POST'])
def add_report():
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO reports (P_ID, D_ID, Test_Type, Report_Date, Result) VALUES (%s,%s,%s,%s,%s)",
                (request.form['p_id'], request.form['d_id'], request.form['test'], request.form['date'], request.form['result']))
    db.commit()
    return redirect('/reports')

@app.route('/view_report/<int:report_id>')
def view_report(report_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""SELECT r.*, p.First_Name as Patient_FirstName, p.Last_Name as Patient_LastName,
                   e.First_Name as Doctor_FirstName, e.Last_Name as Doctor_LastName
                   FROM reports r
                   JOIN patient p ON r.P_ID = p.P_ID
                   JOIN doctor d ON r.D_ID = d.D_ID
                   JOIN employee e ON d.D_ID = e.E_ID
                   WHERE r.R_ID = %s""", (report_id,))
    report = cur.fetchone()
    return render_template('view_report.html', report=report)

@app.route('/delete_report/<int:report_id>')
def delete_report(report_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM reports WHERE R_ID = %s", (report_id,))
    db.commit()
    return redirect('/reports')

@app.route('/rooms')
def rooms():
    db = get_db()
    cur = db.cursor(dictionary=True)
    
    # Handle search functionality
    search_query = request.args.get('q', '')
    if search_query:
        cur.execute("SELECT * FROM rooms WHERE Room_ID LIKE %s OR Type LIKE %s OR Availability LIKE %s OR Capacity LIKE %s", 
                   (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
    else:
        cur.execute("SELECT * FROM rooms")
    
    return render_template('rooms.html', rooms=cur.fetchall(), search_query=search_query)

@app.route('/add_room', methods=['POST'])
def add_room():
    db = get_db()
    cur = db.cursor()
    # Set default capacity based on room type
    capacity_map = {
        'ICU': 1,
        'Private': 1,
        'Semi-Private': 2,
        'General': 4,
        'Maternity': 2,
        'Pediatric': 3
    }
    room_type = request.form['type']
    capacity = capacity_map.get(room_type, 1)  # Default to 1 if type not found
    
    cur.execute("INSERT INTO rooms (Room_ID, Capacity, Type, Availability) VALUES (%s,%s,%s,%s)",
                (request.form['room_id'], capacity, room_type, request.form['availability']))
    db.commit()
    return redirect('/rooms')

@app.route('/toggle_room_status/<int:room_id>')
def toggle_room_status(room_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT Availability FROM rooms WHERE Room_ID = %s", (room_id,))
    room = cur.fetchone()
    
    if room:
        if room['Availability'] == 'Available':
            new_status = 'Occupied'
        elif room['Availability'] == 'Occupied':
            new_status = 'Available'
        elif room['Availability'] == 'Reserved':
            new_status = 'Occupied'
        else:
            new_status = 'Available'  # Default for other statuses
        
        cur.execute("UPDATE rooms SET Availability = %s WHERE Room_ID = %s", (new_status, room_id))
        db.commit()
    
    return redirect('/rooms')

@app.route('/delete_room/<int:room_id>')
def delete_room(room_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM rooms WHERE Room_ID = %s", (room_id,))
    db.commit()
    return redirect('/rooms')

if __name__ == '__main__':
    app.run(debug=True)
