import sr_dev_resume_and_cv_tailor
import web_scraper
import lib
import sys

resume_file_path = "resume.txt"

url = sys.argv[1]

job_description = web_scraper.get_job_description_from_indeed(url);

resume, cover_letter = sr_dev_resume_and_cv_tailor.generate_resume_and_cover_letter(job_description)

formatted_resume = lib.find_and_replace(resume, "*", "")

with open(resume_file_path, 'w', encoding='utf-8') as file:
    file.write(formatted_resume)

lib.remove_blank_lines(resume_file_path)
