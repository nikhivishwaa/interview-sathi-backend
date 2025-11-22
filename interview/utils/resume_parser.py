from pdfminer.high_level import extract_text
import re
from typing import Union, IO

def parse_resume_text(source: Union[str, IO[bytes]]):
    try:
        text = extract_text(source)
        return text
    except Exception:
        return ""


def clean_resume_text(raw_text):
    # Remove extra whitespaces
    text = re.sub(r'\s{2,}', ' ', raw_text)

    # Break on periods followed by uppercase (e.g. sentence end)
    text = re.sub(r'\. (?=[A-Z])', '.\n\n', text)

    # Restore bullet-style or section-based line breaks
    text = re.sub(r'(•|\*)', r'\n\n•', text)

    # Attempt to preserve some tabs (like section titles)
    text = re.sub(
        r'(SUMMARY|KEYEXPERTISE|EDUCATIONAL|CERTIFICATIONS|PROJECTS|PERSONALINFORMATION|REFERENCES|HOBBIES|ACTIVITIES|TRAINING)',
        r'\n\n\1\n\n',
        text,
        flags=re.IGNORECASE,
    )

    return text.strip()
