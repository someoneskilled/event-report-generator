# RepGEN - Event Report Generator

## Overview

This project is an **AI-powered Event Report Generator** web application built using **Flask**. It allows users to submit event details through a form, upload related files, and automatically generate a structured event report. The generated report includes key details, objectives, feedback, and a summary. Additionally, the app supports image captioning, file uploads, and provides the option to download the report in DOCX format.

Key features of the application:
- **Form-Based Data Collection**: Users input event information such as event details, time, objectives, and feedback.
- **File Uploads**: Users can upload event-related files, including images and documents.
- **AI-Powered Text Generation**: AI generates structured content like event summaries, objectives, feedback, and outcomes.
- **File Captioning**: Automatically generates captions for uploaded images using AI.
- **Report Download**: Users can download the final event report as a DOCX file.

## Technologies Used
- **Flask**: A lightweight Python web framework used for building the web app.
- **Jinja2**: Templating engine used for rendering dynamic HTML content.
- **Python-docx**: Used for generating DOCX reports.
- **OpenAI GPT-3 / LLaMA-3.2 Vision**: For text generation and image captioning.
- **HTML/CSS**: Frontend for designing the user interface.

## Features

### 1. **Form Submission**:
   - Event details, objectives, feedback, and outcomes can be entered via a user-friendly form.
   - The form includes input fields for event time, description, goals, and more.

### 2. **File Uploads**:
   - Users can upload multiple event-related files, including images (JPG, PNG, JPEG) and other documents.
   - Uploaded images are automatically captioned using the AI model, which generates descriptions for the images.

### 3. **Report Generation**:
   - Based on the submitted data, the application generates an event report that includes:
     - Event overview (summary)
     - Event objectives
     - Event feedback
     - Event outcomes
   - The report is displayed in the web interface and can be downloaded as a DOCX file.

### 4. **Time Formatting**:
   - The app converts event start and end times into a 12-hour AM/PM format.
   - It also calculates and displays the event duration in hours and minutes.

### 5. **Image Display**:
   - Images uploaded by the user are displayed in a grid format on the summary page with their captions below them.

## Setup Instructions

### Prerequisites
- Python 3.6+
- Virtual environment (recommended)
- Dependencies listed in `requirements.txt`

### Installation

## Clone this repository:
   ```bash
   git clone https://github.com/yourusername/event-report-generator.git
   cd event-report-generator
   ```





### 1. Create a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

### 2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set up a folder for file uploads (ensure the `UPLOAD_FOLDER` is correctly set in the Flask app):

```bash
mkdir uploads
```

### 4. Run the Flask app:

```bash
python app.py
```

### 5. Open your web browser and navigate to `http://127.0.0.1:5000` to access the application.

---

## File Structure

```
event-report-generator/
│
├── app.py                   # Main Flask app file
├── templates/                # HTML templates for the web app
│   ├── form.html             # Form for user input
│   ├── summary.html          # Summary page after form submission
│
├── static/                   # Static files (CSS, JS, images, etc.)
│   ├── uploads/              # Folder for storing uploaded files
│
├── requirements.txt          # List of project dependencies
├── README.md                 # Project documentation
```

---

## How to Use

### 1. Fill Out the Form:

- Visit the home page (/), where you can input event details including the event title, description, objectives, feedback, and the event time.
- You can also upload images or documents that are related to the event.

### 2. View the Summary:

- After submitting the form, you'll be directed to the summary page (/summary).
- The page will display the event details, AI-generated content (summary, objectives, feedback), and the uploaded files with captions.

### 3. Download the Report:

- On the summary page, you can click on the "Download as Docx" button to download the generated report in DOCX format.

---

## Limitations

- Currently, only images in JPG, PNG, and JPEG formats are supported for upload.
- The event duration is fixed to 50 minutes per session in the current implementation.
- The application assumes correct input formats for event time and data fields.

---

## Future Improvements

- Support for more file formats (PDF, DOCX, etc.)
- Enhanced AI-powered analysis for feedback and outcomes
- Admin dashboard for viewing all submitted reports and managing files

