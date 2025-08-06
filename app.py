
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import csv
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
SUBMISSION_FOLDER = 'submissions'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SUBMISSION_FOLDER, exist_ok=True)

exams = {}
csv_log = os.path.join(SUBMISSION_FOLDER, 'submissions.csv')

@app.route('/')
def home():
    return redirect(url_for('student_login'))

@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_name = request.form['student_name'].strip()
        exam_code = request.form['exam_code'].strip()
        return redirect(url_for('student_exam', code=exam_code, name=student_name))
    return render_template('student_login.html')

@app.route('/exam/<code>', methods=['GET', 'POST'])
def student_exam(code):
    exam = exams.get(code)
    student_name = request.args.get('name', '')
    if request.method == 'POST':
        answer = request.form['answer']
        timestamp = datetime.now().isoformat()
        filename = f'{code}_{student_name}.txt'
        filepath = os.path.join(SUBMISSION_FOLDER, filename)
        with open(filepath, 'w') as f:
            f.write(f"Student: {student_name}\nTime: {timestamp}\n\n{answer}")
        with open(csv_log, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([student_name, code, timestamp, filename])
        return render_template('submitted.html')
    return render_template('student_exam.html', exam=exam, student_name=student_name, code=code)

@app.route('/teacher/upload', methods=['GET', 'POST'])
def teacher_upload():
    if request.method == 'POST':
        uploaded_file = request.files['exam_file']
        if uploaded_file:
            code = str(len(exams) + 1001)
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)
            exams[code] = uploaded_file.filename
            return f"✅ Exam uploaded. Exam Code: {code}<br><a href='/teacher/dashboard'>Go to Dashboard</a>"
    return render_template('teacher_upload.html')

@app.route('/teacher/dashboard')
def teacher_dashboard():
    submissions = os.listdir(SUBMISSION_FOLDER)
    return render_template('teacher_dashboard.html', submissions=submissions)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/submissions/<filename>')
def view_submission(filename):
    return send_from_directory(SUBMISSION_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
