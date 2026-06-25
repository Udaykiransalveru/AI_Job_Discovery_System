from services.parser import (
    extract_text_from_pdf,
    extract_skills
)

text = extract_text_from_pdf("resume.pdf")

skills = extract_skills(text)

print(skills)