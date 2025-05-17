import os
import json
from datetime import datetime

# List of predefined categories
CATEGORIES = [
    "Java Developer", "PHP Developer", "Android Developer", "Content Writer",
    "Business Development Manager", "Software Engineer", "Graphic Designer",
    "Business Analyst", "Data Engineer", "Project Manager", "Sales Manager",
    "Sales Executive", "HR Manager", "Data Scientist", "Civil Engineer",
    "Senior Consultant"
]

# Base paths
BASE_DIR = "jobs"
DATA_FILE = "data/jobs.json"
ASSETS_DIR = "assets"

# Ensure directories exist
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# Select category
print("Select a job category:")
for idx, cat in enumerate(CATEGORIES, 1):
    print(f"  {idx}. {cat}")
cat_index = int(input(f"Enter number (1-{len(CATEGORIES)}): ")) - 1
category = CATEGORIES[cat_index]
category_slug = category.lower().replace(" ", "-")

def safe_input(prompt_text, default=None, multiline=False):
    if multiline:
        print(f"{prompt_text} (type END on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line.replace('"', ''))  # Remove quotes
        return "\n".join(lines)
    else:
        val = input(f"{prompt_text}{' [' + default + ']' if default else ''}: ").strip()
        val = val.replace('"', '')  # Remove quotes
        return val if val else default

# Prompt for job data
def prompt(label, default=None):
    val = safe_input(f"{label}{' [' + default + ']' if default else ''}: ")
    return val if val else default

role = prompt("Role")
company = prompt("Company name")
payscale = prompt("Payscale", "Undisclosed")
location = prompt("Location")
# location = prompt("Location","Undisclosed")
experience = prompt("Experience", "Undisclosed")
# positions = prompt("Positions open", "Undisclosed")
positions = prompt("Positions open")
skills = prompt("Key skills (comma-separated)")

print("Enter 'About the company' (type END on a new line to finish):")
about_lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    about_lines.append(line)
about = "\n".join(about_lines)

print("Enter 'Job Description' (type END on a new line to finish):")
jd_lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    jd_lines.append(line)
description = "\n".join(jd_lines)

# Key details
job_function = prompt("Job Function")
industry = prompt("Industry")
specialization = prompt("Specialization")
qualification = prompt("Qualification")
employment = prompt("Employment Type")

apply_url = prompt("Apply URL")
posted_by = prompt("Posted By (Company Name)", company)

# Create job ID using Unix timestamp
timestamp = int(datetime.now().timestamp())
jobid = str(timestamp)
dt_object = datetime.fromtimestamp(timestamp)
ftdate = dt_object.strftime('%d-%b-%Y')
job_path = f"jobs/{category_slug}/{jobid}/"

# Create job directory
os.makedirs(os.path.join(BASE_DIR, category_slug, jobid), exist_ok=True)

# Create or append to jobs.json
new_entry = {
    "category": category_slug,
    "role": role,
    "company": company,
    "payscale": payscale,
    "location": location,
    "experience": experience,
    "position-open": positions,
    "key-skills": skills,
    "about": about,
    "description": description,
    "key-details": {
        "job-function": job_function,
        "industry": industry,
        "specialization": specialization,
        "qualification": qualification,
        "employment-type": employment
    },
    "url-apply": apply_url,
    "posted-by": posted_by,
    "path": job_path,
    "timestamp": timestamp,
    "jobid": jobid
}

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            jobs = json.load(f)
        except json.JSONDecodeError:
            jobs = []
else:
    jobs = []

jobs.append(new_entry)

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2, ensure_ascii=False)

html_path = os.path.join(BASE_DIR, category_slug, jobid, "index.html")
skills_html = ''.join([f"<span>{s.strip()}</span>" for s in (skills or "").split(",") if s.strip()])
related_jobs = [j for j in jobs if j["category"] == category_slug and j["jobid"] != jobid][:4]

# Format bold and bullet points in description
import re
desc_formatted = re.sub(r"\$\%(.*?)\%\$", r"<strong>\1</strong>", description)
desc_formatted = re.sub(r"\*(.*?)\*", r"<ul><li>\1</li></ul>", desc_formatted)
desc_formatted = desc_formatted.replace("\\n", "<br>")
desc_formatted = desc_formatted.replace("\n", "<br>")

about_formatted = re.sub(r"\$\%(.*?)\%\$", r"<strong>\1</strong>", about)
about_formatted = re.sub(r"\*(.*?)\*", r"<ul><li>\1</li></ul>", about_formatted)
about_formatted = about_formatted.replace("\\n", "<br>")
about_formatted = about_formatted.replace("\n", "<br>")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{role} at {company}</title>
  
  <meta name="description" content="{role} in {location if location else ""} at {company} with {experience} experience is required - Number of position are {positions}">
  <meta property="og:title" content="{role} | {company}">
  <meta property="og:description" content="{payscale} | {experience} | {location}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{job_path}">
  <meta property="og:image" content="/assets/cp.svg">
  <link rel="icon" type="image/png" href="/assets/cp.svg">
  <link rel="stylesheet" href="/assets/style.css">
</head>

<body>
  <div class="container">
  
    <div class="top-nav-bar">
      <button class="back-button" id="backBtn" title="Go Back">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="#333" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6" />
        </svg>
      </button>
      <div class="nav-title">Job Detail</div>
    </div>
    
    <div>
      <section id="jobcard">
        <div class="job-card">
          <img src="/assets/cp.svg" alt="Company Logo" width="50">
          <h1>{role}</h1>
          <div class="job-meta">{company} – {location if location else ""} | {ftdate}</div>
          <div class="skills">{skills_html if skills_html else ""}</div>
          <div class="pa">
            {'<div class="child"><img src="/assets/jd-exp.svg"><p>' + experience + '</p></div>' if experience else ''}
            {'<div class="child"><img src="/assets/srp-location.svg"><p>' + location + '</p></div>' if location else ''}
            {'<div class="child"><img src="/assets/jd-salary.svg"><p>' + payscale + '</p></div>' if payscale else ''}
            {'<div class="child"><img src="/assets/vacancies-icon.svg"><p>' + positions + '</p></div>' if positions else ''}
          </div>
        </div>
      </section>

      <section id="Details">
        {f'<section id="about-company" class="job-card"><h2>About Company</h2><p>{about_formatted}</p></section>' if about_formatted.strip() else ''}
        
        {f'<section id="jd" class="job-card"><h2>Job Description</h2><p>{desc_formatted}</p></section>' if desc_formatted.strip() else ''}

       {f"""
      <section id="kd" class="job-card key-details">
        <h2>Key Details</h2>
        <div class="details-grid">
          {f"<div><span class='label'>Function</span><span class='value'>{job_function}</span></div>" if job_function else ""}
          {f"<div><span class='label'>Industry</span><span class='value'>{industry}</span></div>" if industry else ""}
          {f"<div><span class='label'>Specialization</span><span class='value'>{specialization}</span></div>" if specialization else ""}
          {f"<div><span class='label'>Qualification</span><span class='value'>{qualification}</span></div>" if qualification else ""}
          {f"<div><span class='label'>Employment Type</span><span class='value'>{employment}</span></div>" if employment else ""}
        </div>
      </section>
      """ if any([job_function, industry, specialization, qualification, employment]) else ''}

        {f'<section id="ks" class="job-card"><h3>Key Skills</h3><div class="skills">{skills_html}</div></section>' if skills_html else ''}
        
      {f"""
      <section id=" pby" class="job-card key-details">
        <h2>Job Posted</h2>
        <div class="details-grid">
          {f"<div><span class='label'>Company</span><span class='value'>{company}</span></div>" if company else ""}
        </div>
      </section>
      """ if company else ''}

        

        {f"""
        <section class="si-card">
          <h1>Similar Jobs</h1>
          <div class='job-list'>
          </div>
        </section>"""}
      </section>
    </div>
    
    <div class="sticky-apply-bar" id="stickyApply">
      <button class="share-btn" onclick="" title="Share this job">🔗</button>
      <a href="{apply_url}" target="_blank" class="apply-btn">Apply</a>
    </div>
    
  </div>
  <script src="/assets/si.js"></script>
</body>
</html>
""")

print(f"\n✅ Job '{role}' added successfully at: {job_path}")

