import re

def find_and_replace(text, find_str, replace_str) -> str:
    print(f"Replaced '{find_str}' with '{replace_str}'.")
    return text.replace(find_str, replace_str)

def remove_blank_lines(file_path) -> None:
    with open(file_path, 'r+') as f:
        lines = f .readlines()
        f.seek(0)
        f.writelines(line for line in lines if line.strip())
        f.truncate()
    print(f"Removed blank lines from {file_path}.")

def extract_simple_section(section, text) -> str:
    summary_pattern = rf"{section}\s*(.*?)\n\n"
    match = re.search(summary_pattern,text, re.DOTALL)

    if match:
        print(f"The {section} extracted.")
        return match.group(1)
    else:
        print(f"The {section} not found.")
        return f"No {section} found."

def extract_experience(text) -> str:
    experience_pattern = r"Experience\n(.*?)\nProjects"
    match = re.search(experience_pattern, text, re.DOTALL)
    if match:
        print("Experience extracted.")
        return match.group(1)
    else:
        print("Experience not found.")
        return "No experience found."

def fill_resume_template(template_path, data, output_path):
    doc = Document(template_path)
    for paragraph in doc.paragraphs:
        inline = paragraph.runs
        for i in range(len(inline)):
            text = inline[i].text
            for key, value in data.items():
                text = text.replace('{{' + key + '}}', value)
            inline[i].text = text
    doc.save(output_path)
    print("Resume template filled.")

def write_text_document(file_path, text):
    with open(resume_file_path, 'w') as file:
        file.write(formatted_resume)
    print(f"'{file_path}' written.")

# def format_cover_letter():
