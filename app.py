
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

exams = {}  # in-memory exam storage

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
        os.makedirs('submissions', exist_ok=True)
        with open(f'submissions/{code}_{student_name}.txt', 'w') as f:
            f.write(f"Student: {student_name}\nTime: {timestamp}\n\n{answer}")
        return "✅ Your submission has been recorded!"
    return render_template('student_exam.html', exam=exam, student_name=student_name)

@app.route('/teacher/upload', methods=['GET', 'POST'])
def teacher_upload():
    if request.method == 'POST':
        uploaded_file = request.files['exam_file']
        if uploaded_file:
            code = str(len(exams) + 1001)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)
            exams[code] = uploaded_file.filename
            return f"✅ Exam uploaded. Exam Code: {code}<br>Student URL: /exam/{code}"
    return render_template('teacher_upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
