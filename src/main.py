import google_ai
import web_scraper
import lib
import sys
from docx import Document


resume_file_path: str = "resume.txt"
url: str = sys.argv[1]
job_description: str = web_scraper.get_job_description(url);
google_ai.set_job_description(job_description)
resume: str = google_ai.generate_resume()
formatted_resume: str = lib.find_and_replace(resume, "*", "")
lib.write_text_document(resume_file_path, formatted_resume)
lib.remove_blank_lines(resume_file_path)
summary: str = lib.extract_simple_section("Summary", formatted_resume)
experience: str = lib.extract_experience(formatted_resume)
projects: str = lib.extract_simple_section("Projects", formatted_resume)
skills: str = lib.extract_simple_section("Skills", formatted_resume)
doc_path: str = 'resume_template.docx'
data: object = {
    'summary': summary,
    'experience': experience,
    'projects': projects,
    'skills': skills,
}
lib.fill_resume_template(doc_path, data, 'output_resume.docx')
cover_letter: str = google_ai.generate_cover_letter();
print(cover_letter)
