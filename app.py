from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from groq import Groq
import base64
from docx import Document
from flask import send_file
from io import BytesIO

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

def generate_image_caption(image_path):
    try:
        with open(image_path, "rb") as img_file:
            b64_image = base64.b64encode(img_file.read()).decode("utf-8")
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Give a short one liner tagline for the image of event, no need to give intro just give a few words caption telling whats in the image."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                    ]
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Caption Error: {str(e)}"

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    form_data = {}

    text_fields = [
        "event_title", "web_url", "event_summary", "event_objectives", "event_feedback_bulletin",
        "event_venue", "event_date", "event_department",
        "faculty_coordinator", "chief_guest", "guest_testimonial"
    ]

    for field in text_fields:
        form_data[field] = request.form.get(field)

    if form_data["event_summary"]:
        form_data["event_summary"] = generateAI(
            form_data["event_summary"],
            "You are a professional event summarizer. Convert rough notes into a clear, 150-word summary. Keep it professional, simple and ready for documentation."
        )

    if form_data["event_objectives"]:
        form_data["event_objectives"] = generateAI(
            form_data["event_objectives"],
            "You are an academic writer. Convert these rough event objectives into a clear, professional bullet-point list. Avoid giving any starting or intro."
        )

    if form_data["event_feedback_bulletin"]:
        form_data["event_feedback_bulletin"] = generateAI(
            form_data["event_feedback_bulletin"],
            "Turn these rough notes into a polished feedbacks of the event or agenda in bullet points. Avoid giving any starting or intro just give the bullet points."
        )

    extra_input = f"""
    Summary: {form_data["event_summary"]}
    Objectives: {form_data["event_objectives"]}
    Activities: {form_data["event_feedback_bulletin"]}
    """
    instruction_extra_fields = """
    Based on the provided event summary, objectives, and activities:
    1. Generate simple bullet points for 'Event Outcome' describing what the event achieved.
    2. Generate a few lines 'SEO-Friendly Short Description' for blog/social sharing use.
    Format:
    Event Outcome: <paragraph>
    SEO Description: <line>
    """
    extra_response = generateAI(extra_input.strip(), instruction_extra_fields)

    try:
        lines = extra_response.split("SEO Description:")
        form_data["event_outcome"] = lines[0].replace("Event Outcome:", "").strip()
        form_data["seo_description"] = lines[1].strip()
    except Exception as e:
        form_data["event_outcome"] = "Error generating event outcome."
        form_data["seo_description"] = "Error generating SEO description."

    form_data['event_time'] = request.form.getlist('event_time')

    file_fields = {
        'poster': None,
        'certificates': [],
        'event_photos': []
    }

    for key in ['poster']:
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

    image_captions = {}
    for photo_filename in file_fields["event_photos"]:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        caption = generate_image_caption(image_path)
        image_captions[photo_filename] = caption

    session['form_data'] = form_data
    session['image_captions'] = image_captions

    data = {
        "form_data": form_data,
        "file_fields": file_fields,
        "image_captions": image_captions
    }

    return render_template("summary.html", data=data)

@app.route('/download-docx')
def download_docx():
    form_data = session.get('form_data')
    image_captions = session.get('image_captions')

    if not form_data:
        return "No data to export."

    doc = Document()
    doc.add_heading('Event Summary Report', 0)

    basic_fields = [
        ("Department", form_data.get("event_department", "")),
        ("Title", form_data.get("event_title", "")),
        ("Venue", form_data.get("event_venue", "")),
        ("Date", form_data.get("event_date", "")),
        ("Time(s)", ", ".join(form_data.get("event_time", []))),
        ("Faculty Coordinator", form_data.get("faculty_coordinator", "")),
        ("Chief Guest", form_data.get("chief_guest", "")),
        ("Web Link", form_data.get("web_url", ""))
    ]

    for label, value in basic_fields:
        doc.add_paragraph(f"{label}: {value}")

    sections = {
        "Event Summary": form_data.get("event_summary", ""),
        "Objectives": form_data.get("event_objectives", ""),
        "Event Feedback": form_data.get("event_feedback_bulletin", ""),
        "Event Outcome": form_data.get("event_outcome", ""),
        "SEO Description": form_data.get("seo_description", "")
    }

    for title, content in sections.items():
        doc.add_heading(title, level=1)
        doc.add_paragraph(content)

    if image_captions:
        doc.add_heading("Photo Captions", level=1)
        for image, caption in image_captions.items():
            doc.add_paragraph(f"{image}: {caption}")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name="summary.docx", mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

if __name__ == '__main__':
    app.run(debug=True)
