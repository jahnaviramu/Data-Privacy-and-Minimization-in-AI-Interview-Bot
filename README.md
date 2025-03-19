AI INTERVIEW BOT WITH RESUME PARSING, DYNAMIC QUESTIONING, AND FEEDBACK SCORE

DESCRIPTION  
This project is an AI-powered interview bot that automates technical interviews by:  
- Parsing resumes to extract key skills, projects, and education details.  
- Generating dynamic interview questions based on the extracted skills.  
- Masking personal details (names, emails, phone numbers, URLs) for privacy compliance.  
- Providing feedback scores by comparing answers to expected responses.  
- Ensuring GDPR compliance with user consent management and secure file handling.  

TECH STACK  
- Backend: Flask (Python)  
- Frontend: HTML, CSS, JavaScript  
- NLP & Parsing: PyMuPDF, Regex, NLTK  
- Summarization: Hugging Face Transformers (facebook/bart-large-cnn)  
- File Encoding: Base64 for secure resume handling  
- Session Management: Flask sessions for tracking interview progress  

KEY FEATURES  

APPLICATION FRAMEWORK AND ARCHITECTURE  
- Framework: Flask handles the backend logic.  
- Frontend: HTML, CSS, and JavaScript for a responsive and user-friendly UI.  
- RESTful API: Flask endpoints manage:  
  - Resume uploads.  
  - Interview initialization and question generation.  
  - Answer submission and scoring.  
  - Fetching encoded and parsed data.  

FRONTEND TECHNOLOGIES  
- HTML (Structure):  
  - Pages include index.html (main interface) and privacy_policy.html (GDPR compliance).  
  - Key elements:  
    - File input for resume uploads.  
    - Chat interface for interview interactions.  
    - Modals for displaying parsed data, summaries, and encoded files.  
- CSS (Styling):  
  - styles.css enhances the appearance with:  
    - Dark blue theme.  
    - Responsive layout.  
    - Custom buttons and input fields.  
- JavaScript (Interactivity):  
  - app.js handles:  
    - Fetching data from Flask endpoints.  
    - Dynamically displaying modals.  
    - Auto-scrolling the chat interface.  
    - Real-time updates for scores and parsed data.  

GDPR COMPLIANCE  
- Consent Modal:  
  - Displayed on application launch using JavaScript.  
  - Requires user consent before processing files.  
- Endpoint: /accept_gdpr (POST)  
  - Stores consent status in Flask sessions.  

RESUME PARSING  
- File Handling:  
  - Uploaded resumes are saved securely using os.  
  - Files are encoded with Base64 for added security.  
- PDF Parsing:  
  - Library: PyMuPDF (fitz) extracts text from PDF files.  
  - Masks sensitive data (emails, phone numbers, URLs) using regex.  
- Data Extraction:  
  - Key sections: Skills, projects, education, and extracurricular activities.  
  - skills_extractor.py:  
    - extract_technical_skills: Identifies common skills (Python, Java, Flask, etc.).  
    - extract_projects: Extracts project details.  
    - extract_education: Identifies degrees and institutions.  

QUESTION BANK AND INTERVIEW MANAGEMENT  
- Question Bank:  
  - File: questions.json.  
  - Contains predefined technical questions categorized by skill.  
- Dynamic Question Generation:  
  - If a skill doesn’t have a predefined question, the bot generates questions dynamically.  
  - Example:  
    "Can you explain your experience with {skill}?"  
- Endpoints:  
  - /start_interview (POST) → Generates a list of questions based on resume skills.  
  - /submit_answer (POST) → Compares answers to expected ones and calculates scores.  

SCORING SYSTEM  
- Libraries:  
  - NLTK:  
    - Tokenizes answers.  
    - Removes stopwords and punctuation.  
  - string: Handles punctuation removal.  
- Logic:  
  - train.py → score_answer() function:  
    - Compares tokenized words from user answers with expected answers.  
    - Calculates a similarity score (0-10 scale).  

SUMMARIZATION AND KEY FIELDS  
- Summarizer:  
  - Library: Hugging Face Transformers.  
  - Model: facebook/bart-large-cnn for concise summaries.  
- Key Fields:  
  - Extracted data is displayed in a structured format:  
    - Top skills, certificates, and projects.  
- Endpoints:  
  - /get_summary (GET) → Fetches summarized resume content.  
  - /get_key_fields (GET) → Displays extracted resume data.  

ENCODED FILE HANDLING  
- Encoding and Decoding:  
  - Library: base64.  
  - Files are encoded before storage and retrieved in Base64 format for secure display.  
- Functions:  
  - encode_file: Saves the encoded content with .enc extension.  
  - decode_file: Reconstructs the original file from encoded data.  
- Endpoint:  
  - /get_encoded_file (GET) → Provides Base64 content of uploaded files.  

SESSION MANAGEMENT  
- Flask Sessions:  
  - Stores user consent and interview state.  
  - Tracks:  
    - Current question index.  
    - Total score and number of questions.  
- File Deletion:  
  - Users can delete uploaded resumes or choose to retain them.  
- Endpoint:  
  - /quit (POST) → Clears session data and optionally deletes files.  

FRONTEND INTERACTION  
- Chat Interface:  
  - Dynamically displays questions, answers, and feedback scores.  
  - Auto-scroll ensures new content is visible.  
- Modals:  
  - Display parsed data, summaries, and encoded files.  
  - Enhances the user experience with interactive pop-ups.  

SECURITY FEATURES  
- GDPR Compliance:  
  - Enforces consent before accessing core functionalities.  
- File Encoding:  
  - Protects sensitive documents by encoding before storage.  
- Input Validation:  
  - Ensures only valid resume formats (e.g., PDF) are processed.  
- Session Management:  
  - Prevents unauthorized access by isolating sessions.  

DEPLOYMENT  
- Server:  
  - The Flask app runs on a Python server (app.py).  
  - Configured for production with debug mode disabled.  
- Static Files:  
  - CSS, JS, and assets served via Flask's url_for() function.  

INSTALLATION AND USAGE  
1. Clone the repository:  
git clone <repository_url>  
cd ai-interview-bot  

2. Install dependencies:  
pip install -r requirements.txt  

3. Run the server:  
python app.py  

4. Open in browser:  
http://localhost:5000  

CONTRIBUTIONS  
Feel free to contribute by submitting a pull request.  

LICENSE  
This project is licensed under the MIT License.  

AI Interview Bot → Automating interviews with AI-powered resume parsing, dynamic questions, and feedback scoring.
