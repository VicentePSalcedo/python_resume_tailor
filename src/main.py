import google_ai
import web_scraper
import lib
import sys

resume_file_path: str = "resume.txt"

url: str = sys.argv[1]

job_description: str = web_scraper.get_job_description_from_indeed(url);

google_ai.set_job_description(job_description)

resume = google_ai.generate_resume()
formatted_resume: str = lib.find_and_replace(resume, "*", "")
# with open(resume_file_path, 'w') as file:
#    file.write(formatted_resume)
# lib.remove_blank_lines(resume_file_path)
print(formatted_resume)

# cover_letter = google_ai.generate_cover_letter();
# print(cover_letter)
