import time
import google.generativeai as genai

genai.configure(api_key="AIzaSyAKjCq_fQZPtlmXFFPhiFugFtVKJUxmNmg")

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

def generate_resume_and_cover_letter(job_description):
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

# TODO Make these files available on the local file system
# You may need to update the file paths
    files = [
        upload_to_gemini("Resume241114.pdf", mime_type="application/pdf"),
    ]

# Some files have a processing delay. Wait for them to be ready.
    wait_for_files_active(files)

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "As a senior recruiter take the following resume:",
            files[0],
            "And tailor it to the following job description. Ensure that the final resume fits on one page and that any blanks are filled in with typical examples.",
        ],
        },
    ]
    )

    response = chat_session.send_message(job_description)

    resume = response.text

    response = chat_session.send_message("Then, provide a cover letter with a tailored resume without a heading; infer the company name from the job description.")

    cover_letter = response.text

    print("Finished generating resume and cover letter")

    return (resume, cover_letter)
