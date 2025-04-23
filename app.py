from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
import pdfkit

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    form_data = {}

    # Text fields
    text_fields = [
        "event_title", "event_summary", "event_objectives", "event_activities",
        "event_venue", "event_date", "event_department",
        "faculty_coordinator", "student_coordinator", "chief_guest"
    ]
    for field in text_fields:
        form_data[field] = request.form.get(field)

    # Time slots (multiple)
    form_data['event_time'] = request.form.getlist('event_time')

    # File uploads
    file_fields = {
        'poster': None,
        'certificates': [],
        'feedback_excel': None,
        'participant_list': None,
        'presenter_list': None,
        'winner_list': None,
        'event_photos': []
    }

    for key in ['poster', 'feedback_excel', 'participant_list', 'presenter_list', 'winner_list']:
        file = request.files.get(key)
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            file_fields[key] = filename

    for key in ['certificates', 'event_photos']:
        uploaded_files = request.files.getlist(key)
        paths = []
        for file in uploaded_files:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                paths.append(filename)
        file_fields[key] = paths

    data = {"form_data": form_data, "file_fields": file_fields}
    
    return render_template("summary.html", data=data)

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    data = request.form['html_data']
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], "report.pdf")
    pdfkit.from_string(data, pdf_path)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
