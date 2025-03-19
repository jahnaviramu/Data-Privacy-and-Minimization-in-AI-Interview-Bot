import fitz  # PyMuPDF for PDF text extraction
import re  # Regular expressions for pattern matching
import json  # For JSON serialization of parsed data

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF, or an empty string if extraction fails.
    """
    try:
        document = fitz.open(pdf_path)  # Open the PDF file
        text = ""
        # Iterate through each page in the PDF and extract text
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        # Handle errors during text extraction
        print(f"Error extracting text from PDF: {e}")
        return ""


def mask_sensitive_data(text):
    """
    Mask sensitive data such as email addresses, phone numbers, and URLs.

    Args:
        text (str): Input text containing sensitive data.

    Returns:
        str: Text with sensitive data masked.
    """
    try:
        # Mask email addresses
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL REDACTED]', text)
        # Mask phone numbers
        text = re.sub(r'\b(\+?\d{1,3})?\s?[-.]?\d{10}\b', '[PHONE REDACTED]', text)
        # Mask LinkedIn and GitHub URLs
        text = re.sub(r'(linkedin\.com/\S+|github\.com/\S+)', '[LINK REDACTED]', text)
        return text
    except Exception as e:
        # Handle errors during masking
        print(f"Error masking sensitive data: {e}")
        return text


def extract_technical_skills(text):
    """
    Extract technical skills from the resume text.

    Args:
        text (str): Input text.

    Returns:
        list: List of found technical skills.
    """
    # Predefined list of technical skills to search for
    skills = [
        'python', 'java', 'c++', 'html', 'css', 'javascript', 'sql', 'machine learning', 'data science',
        'ruby', 'go', 'swift', 'kotlin', 'matlab', 'r', 'php', 'scala', 'react', 'angular', 'django', 'flask',
        'docker', 'aws', 'azure', 'git', 'linux', 'node.js', 'tensorflow', 'pytorch', 'android', 'ios'
    ]
    # Match skills in the text using regular expressions
    found_skills = [skill for skill in skills if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]
    return found_skills


def extract_projects(text):
    """
    Extract project details from the resume text.

    Args:
        text (str): Input text.

    Returns:
        list: List of projects.
    """
    # Define a pattern to match project-related sections
    project_pattern = r'(projects?|project experience)\s*[:\-\n]*([\s\S]*?)(\n\n|\Z)'
    matches = re.findall(project_pattern, text, re.IGNORECASE)
    # Extract and clean project descriptions
    return [match[1].strip() for match in matches]


def extract_education(text):
    """
    Extract education details from the resume text.

    Args:
        text (str): Input text.

    Returns:
        list: List of education details.
    """
    # Define a pattern to match education-related sections
    education_pattern = r'(education|academic background)\s*[:\-\n]*([\s\S]*?)(\n\n|\Z)'
    matches = re.findall(education_pattern, text, re.IGNORECASE)
    # Extract and clean education details
    return [match[1].strip() for match in matches]


def extract_extracurricular_activities(text):
    """
    Extract extracurricular activities from the resume text.

    Args:
        text (str): Input text.

    Returns:
        list: List of extracurricular activities.
    """
    # Define a pattern to match extracurricular activities or hobbies
    activities_pattern = r'(extracurricular activities|volunteer work|hobbies|interests)\s*[:\-\n]*([\s\S]*?)(\n\n|\Z)'
    matches = re.findall(activities_pattern, text, re.IGNORECASE)
    # Extract and clean activity descriptions
    return [match[1].strip() for match in matches]


def get_resume_details(pdf_path):
    """
    Parse the resume and extract key details such as technical skills, projects, education, and extracurricular activities.

    Args:
        pdf_path (str): Path to the resume PDF.

    Returns:
        dict: Parsed resume details, or an empty dictionary if text extraction fails.
    """
    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("Failed to extract text from the PDF.")
        return {}

    # Mask sensitive data before analysis
    masked_text = mask_sensitive_data(text)

    # Extract key details from the text
    technical_skills = extract_technical_skills(masked_text)
    projects = extract_projects(masked_text)
    education = extract_education(masked_text)
    extracurricular_activities = extract_extracurricular_activities(masked_text)

    # Return a dictionary containing all extracted details
    return {
        "technical_skills": technical_skills,
        "projects": projects,
        "education": education,
        "extracurricular_activities": extracurricular_activities
    }


if __name__ == "__main__":
    # Specify the path to the resume PDF
    pdf_path = "path_to_resume.pdf"  # Replace with the actual file path
    # Extract and print resume details in JSON format
    details = get_resume_details(pdf_path)
    print(json.dumps(details, indent=2))
