from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Initialize the Groq client
client = Groq(api_key=api_key)

def generateAI(input_text, instruction):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": input_text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            top_p=1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

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

    # Apply AI generation where needed
    if form_data["event_summary"]:
        form_data["event_summary"] = generateAI(
            form_data["event_summary"],
            "You are a professional event summarizer. Convert rough notes into a clear, 150-word summary."
        )

    if form_data["event_objectives"]:
        form_data["event_objectives"] = generateAI(
            form_data["event_objectives"],
            "You are an academic writer. Convert these rough event objectives into a clear, professional bullet-point list.Avoid giving any starting or intro."
        )

    if form_data["event_activities"]:
        form_data["event_activities"] = generateAI(
            form_data["event_activities"],
            "You are a professional event writer. Turn these rough notes into a polished description of the event activities or agenda in bulletin and Avoid giving any starting or intro."
        )

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

if __name__ == '__main__':
    app.run(debug=True)
