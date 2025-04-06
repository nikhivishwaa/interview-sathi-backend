from pdfminer.high_level import extract_text
import re

def parse_resume_text(file_path):
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        return ""


def clean_resume_text(raw_text):
    # Remove extra whitespaces
    text = re.sub(r'\s{2,}', ' ', raw_text)

    # Break on periods followed by uppercase (e.g. sentence end)
    text = re.sub(r'\. (?=[A-Z])', '.\n\n', text)

    # Restore bullet-style or section-based line breaks
    text = re.sub(r'(•|\*)', r'\n\n•', text)

    # Attempt to preserve some tabs (like section titles)
    text = re.sub(r'(SUMMARY|KEYEXPERTISE|EDUCATIONAL|CERTIFICATIONS|PROJECTS|PERSONALINFORMATION|REFERENCES|HOBBIES|ACTIVITIES|TRAINING)',
                  r'\n\n\1\n\n', text, flags=re.IGNORECASE)

    return text.strip()
