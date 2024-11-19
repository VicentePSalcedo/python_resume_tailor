import time
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ.get('GOOGLE_GENERATIVE_AI_API_KEY'))

job_description: str = ''

def upload_to_gemini(path, mime_type=None):
  file = genai.upload_file(path, mime_type=mime_type)
  return file

def wait_for_files_active(files):
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")

def set_job_description(scraped_job_description):
    job_description = scraped_job_description
# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="as a senior recruiter read the following job posting and tailor my resume to match the require skills as best as posible. present only the deliverables",
)
files = [
    upload_to_gemini("Resume.pdf", mime_type="application/pdf"),
]
wait_for_files_active(files)
chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "As a senior recruiter take the following resume:",
            files[0],
            "And tailor it to the following job description. Ensure that the final resume fits on one page and that any blanks are filled in with typical examples. Leave any notes to the end.",
            job_description,
        ],
        },
    ]
)

def generate_resume() -> str:
    response = chat_session.send_message("give me no intro or outro on the resume response")
    resume = response.text
    print("Finished generating resume...")
    return resume

def generate_cover_letter() -> str:
    response = chat_session.send_message("Then, provide a cover letter with a tailored resume without a heading; infer the company name from the job description.")
    cover_letter = response.text
    print("Finished generating cover letter...")
    return cover_letter

