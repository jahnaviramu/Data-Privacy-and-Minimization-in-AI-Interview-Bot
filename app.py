from flask import Flask, render_template, request, jsonify, session
import os
import base64
import PyPDF2
import re
import json
from train import score_answer  # Import function for scoring answers
from privacy import encode_file, decode_file  # Import for file encoding/decoding
from transformers import pipeline, logging  # For NLP summarization
import warnings

warnings.filterwarnings("ignore")

# Suppress detailed logs from the Transformers library
logging.set_verbosity_error()

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

# Define and create the uploads folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables to manage interview state
questions = []
current_question_index = 0
parsed_data = {}
total_score = 0
total_questions = 0


# Middleware to check GDPR consent before processing requests
@app.before_request
def check_gdpr_consent():
    """Ensure GDPR consent before accessing most endpoints."""
    if request.endpoint not in ["index", "privacy_policy", "accept_gdpr", "static"]:
        if not session.get("gdpr_accepted"):
            return jsonify({"error": "GDPR consent is required to use this application."}), 403


@app.route("/accept_gdpr", methods=["POST"])
def accept_gdpr():
    """Handle GDPR acceptance."""
    session["gdpr_accepted"] = True
    return jsonify({"message": "GDPR consent accepted. You can now proceed."})


@app.route("/privacy-policy")
def privacy_policy():
    """Render the Privacy Policy page."""
    return render_template("privacy_policy.html")


@app.route("/")
def index():
    """Render the main application page."""
    return render_template("index.html")


# Load predefined questions from a JSON file
def load_questions():
    """Load questions from the JSON file."""
    try:
        with open("questions.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: 'questions.json' not found.")
        return {}


question_bank = load_questions()

# Initialize the NLP summarizer
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    print(f"Error initializing summarizer: {e}")
    summarizer = None


# Function to parse resume text from a PDF file
def parse_resume(filepath):
    """Extract and parse text from the uploaded resume."""
    text = ""
    if filepath.endswith(".pdf"):
        with open(filepath, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text()

    # Extract relevant sections from the parsed text
    parsed_data = {
        "education": extract_section(text, "Education"),
        "skills": extract_section(text, "Technical skills"),
        "projects": extract_section(text, "Projects"),
        "certificates": extract_section(text, "Certificates and achievements"),
        "extracurricular": extract_section(text, "Extracurricular Activities"),
    }
    return parsed_data


# Function to extract specific sections from text
def extract_section(text, section_name):
    """Extract a specific section from the text based on the section name."""
    pattern = rf"{section_name}\n(.*?)(\n\n|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else "Not found"


@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    """Handle resume upload and parse the content."""
    global parsed_data
    file = request.files.get("resume")
    if not file:
        return jsonify({"message": "No file uploaded."}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    encode_file(file_path)  # Encode file for security

    resume_details = parse_resume(file_path)
    if not resume_details:
        return jsonify({"message": "No details found in the resume."})

    parsed_data = resume_details  # Store the parsed data globally
    return jsonify({"message": "Resume parsed successfully."})


@app.route("/start_interview", methods=["POST"])
def start_interview():
    """Initialize and start the interview process."""
    global questions, current_question_index, total_questions

    technical_skills = parsed_data.get("skills", "")
    if not technical_skills:
        return jsonify({"message": "No technical skills found in the parsed resume."}), 400

    questions = []
    for skill in technical_skills.split(", "):
        if skill.lower() in question_bank:
            questions.extend(question_bank[skill.lower()])
        else:
            questions.append({
                "question": f"Can you explain your experience with {skill}?",
                "expected_answer": f"Experience with {skill}"
            })

    if not questions:
        return jsonify({"message": "No questions available for the extracted skills."})

    total_questions = len(questions)
    current_question_index = 0
    return jsonify({
        "message": "Interview started.",
        "question": questions[current_question_index]["question"]
    })


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    """Handle user's answer submission and provide feedback."""
    global current_question_index, questions, total_score

    user_answer = request.json.get("answer")
    if not user_answer:
        return jsonify({"error": "Please provide an answer!"}), 400

    if current_question_index < len(questions):
        question_data = questions[current_question_index]
        expected = question_data["expected_answer"]
        score = score_answer(expected, user_answer)
        total_score += score  # Update the total score

        current_question_index += 1
        next_question = questions[current_question_index]["question"] if current_question_index < len(
            questions) else None

        return jsonify({
            "user_answer": user_answer,
            "score": score,
            "expected_answer": expected,
            "next_question": next_question or "No more questions."
        })
    return jsonify({"message": "All questions answered."})


@app.route("/get_summary", methods=["GET"])
def get_summary():
    """Generate a summary of the parsed resume data."""
    if not parsed_data:
        return jsonify({"error": "No parsed data available to summarize."}), 404

    full_text = " ".join(parsed_data.values()).strip()
    if not full_text or len(full_text.split()) < 10:
        return jsonify({"error": "Parsed data is too short to generate a summary."}), 400

    if summarizer is None:
        return jsonify({"error": "Summarization model not initialized."}), 500

    try:
        summary = summarizer(full_text, max_length=150, min_length=50, do_sample=False)
        return jsonify({"summary": summary[0]["summary_text"]})
    except Exception as e:
        return jsonify({"error": f"Failed to generate summary: {str(e)}"}), 500


@app.route('/get_score', methods=['GET'])
def get_score():
    """Provide the overall score for the interview."""
    global total_questions, total_score

    if total_questions == 0:
        total_score = 0
        return jsonify({"error": "No questions answered."}), 400

    average_score = total_score / total_questions
    return jsonify({"score": round(average_score, 2)})


@app.route("/quit", methods=["POST"])
def quit_application():
    """
    Handle cleanup tasks like deleting uploaded resumes and resetting the score.
    """
    global total_score, total_questions

    # Fetch file name from request
    file_name = request.json.get("file_name", "")
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    resume_deleted = False

    # Delete the uploaded file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
        resume_deleted = True

    # Reset the score to 0
    total_score = 0
    total_questions = 0

    return jsonify({
        "message": "Quit task completed. Score reset to 0 successfully.",
        "score_displayed": True,
        "resume_deleted": resume_deleted
    })


@app.route("/reset_score", methods=["POST"])
def reset_score():
    """
    Reset the total score and questions to 0 explicitly.
    """
    global total_score, total_questions

    total_score = 0
    total_questions = 0

    return jsonify({"message": "Score reset to 0 successfully."})


@app.route("/get_key_fields", methods=["GET"])
def get_key_fields():
    """Extract and return key fields like skills, projects, and certificates."""
    if not parsed_data:
        return jsonify({"error": "No parsed data available."}), 404

    try:
        certificates = parsed_data.get("certificates", "").split("\n")[:3]
        skills = parsed_data.get("skills", "").split("\n")[0]
        projects = parsed_data.get("projects", "").split("\n•")[:3]

        key_fields = {
            "Top Certificates": certificates,
            "Key Skills": skills,
            "Top Projects": projects
        }
        return jsonify(key_fields)
    except Exception as e:
        return jsonify({"error": f"Failed to extract key fields: {str(e)}"}), 500


@app.route('/get_encoded_file', methods=['GET'])
def get_encoded_file():
    """Provide Base64 encoded content of the uploaded file."""
    try:
        file_path = "resume.pdf"  # Replace with your actual file path
        with open(file_path, "rb") as file:
            encoded_content = base64.b64encode(file.read()).decode("utf-8")

        return jsonify({"encoded_content": encoded_content})
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to encode file: {str(e)}"}), 500


@app.route('/get_parsed_data', methods=['GET'])
def get_parsed_data():
    """Provide parsed resume data."""
    global parsed_data

    if not parsed_data:
        return jsonify({"error": "No parsed data available."}), 404

    return jsonify(parsed_data)


if __name__ == "__main__":
    app.run(debug=False)
