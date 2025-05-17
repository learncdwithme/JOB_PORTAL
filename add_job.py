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
posted_by = prompt("Posted By (Company Name)", company+" - Job Search")

# Create job ID using Unix timestamp
timestamp = str(int(datetime.now().timestamp()))
jobid = timestamp
dt_object = datetime.fromtimestamp(jobid)
ftdate = dt_object.strftime('%d-%b-%Y')
job_path = f"/jobs/{category_slug}/{jobid}/"

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


def get_keywords_for_role(role: str) -> str:
    role_keywords = {
        "Java Developer": "Java jobs, backend developer, Java Spring, software development, Java careers",
        "PHP Developer": "PHP jobs, web development, Laravel, backend programming, full stack PHP",
        "Android Developer": "Android jobs, mobile developer, Kotlin, Android Studio, mobile app development",
        "Content Writer": "content writing, SEO writer, blog writer, freelance writer, digital content",
        "Business Development Manager": "sales strategy, BDM, client acquisition, corporate sales, business growth",
        "Software Engineer": "software development, full stack developer, coding jobs, tech engineer, IT jobs",
        "Graphic Designer": "UI/UX design, Adobe Photoshop, visual design, creative designer, branding",
        "Business Analyst": "data analysis, business strategy, stakeholder analysis, BA jobs, project planning",
        "Data Engineer": "data pipeline, ETL jobs, big data, data warehousing, cloud data engineering",
        "Project Manager": "project delivery, PMP certified, agile project management, PM jobs, team leadership",
        "Sales Manager": "sales leader, B2B sales, territory manager, sales jobs, team sales manager",
        "Sales Executive": "inside sales, outbound sales, telecalling jobs, entry-level sales, field sales",
        "HR Manager": "HRBP, talent acquisition, human resources, employee engagement, HR strategy",
        "Data Scientist": "machine learning, AI jobs, data modeling, Python for data science, data analytics",
        "Civil Engineer": "construction jobs, site engineer, structural design, AutoCAD, civil projects",
        "Senior Consultant": "consulting services, management consultant, client advisory, senior strategy consultant"
    }

    # Provide default fallback if role is not listed
    return role_keywords.get(role, "technology jobs, career opportunities, hiring now, software jobs")



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

# Python-style pseudocode for clarity
company_part = f" at {company}" if company else ""
location_part = f" in {location}" if location else " (Remote or Flexible Location)"
experience_part = f"Experience: {experience}" if experience else ""
payscale_part = f"{payscale} | " if payscale else ""
position_part = f"Number of positions: {positions}" if positions else "Multiple openings available"
role_keywords = f"{role}, {role.lower()} jobs, {role.lower()} openings"
industry_keywords = get_keywords_for_role(role)

json_ld = """
<script type="application/ld+json">
{{
  "@context": "http://schema.org",
  "@type": "JobPosting",
  "title": "{role}",
  "description": "Hiring {role}{company_part}{location_part}. {experience_part} experience. {position_part}.",
  "identifier": {{
    "@type": "PropertyValue",
    "name": "{company}",
    "value": "{job_id}"
  }},
  "datePosted": "{date_posted}",
  "validThrough": "{expiry_date}",
  "employmentType": "Full-time",
  "hiringOrganization": {{
    "@type": "Organization",
    "name": "{company}",
    "sameAs": "{company_website}"
  }},
  "jobLocation": {{
    "@type": "Place",
    "address": {{
      "@type": "PostalAddress",
      "addressLocality": "{location}",
      "addressCountry": "IN"
    }}
  }},
  "baseSalary": {{
    "@type": "MonetaryAmount",
    "currency": "INR",
    "value": {{
      "@type": "QuantitativeValue",
      "value": "{salary_value}",
      "unitText": "YEAR"
    }}
  }}
}}
</script>
""".format(
    role=role,
    company_part=company_part,
    location_part=location_part,
    experience_part=experience_part,
    position_part=position_part,
    company=company,
    job_id=jobid,
    date_posted=timestamp,
    expiry_date=timestamp,
    company_website=apply_url,
    location=location,
    salary_value=payscale
)


with open(html_path, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{role}{company_part}{location_part} | Apply Now</title>
  <meta name="description" content="Looking for a {role} job{company_part}{location_part}? We are hiring skilled professionals with {experience_part} experience. {position_part}">
  <meta name="keywords" content="{role}, {role_keywords}, {company}, {location}, {industry_keywords}, hiring, careers, jobs in {location}, {role} jobs, IT jobs, software careers, remote jobs, tech jobs">

  <meta property="og:title" content="{role}{company_part}{location_part} | Apply Now">
  <meta property="og:description" content="content="Looking for a {role} job{company_part}{location_part}? We are hiring skilled professionals with {experience_part} experience. {position_part}">

  <meta property="og:type" content="website">
  <meta property="og:url" content="{job_path}">
  <meta property="og:image" content="/assets/cp.svg">
  <link rel="stylesheet" href="/assets/style.css">

  {ld}

</head>

<body>
  <div class="container">
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
          {f"<p><strong>Function:</strong> {job_function}</p>" if job_function else ""}
          {f"<p><strong>Industry:</strong> {industry}</p>" if industry else ""}
          {f"<p><strong>Specialization:</strong> {specialization}</p>" if specialization else ""}
          {f"<p><strong>Qualification:</strong> {qualification}</p>" if qualification else ""}
          {f"<p><strong>Employment Type:</strong> {employment}</p>" if employment else ""}
        </section>""" if any([job_function, industry, specialization, qualification, employment]) else ''}

        {f'<section id="ks" class="job-card"><h3>Key Skills</h3><div class="skills">{skills_html}</div></section>' if skills_html else ''}

        {f"""
        <section class="si-card">
          <h1>Similar Jobs</h1>
          <div class='job-list'>
          </div>
        </section>""" if related_jobs else ''}
      </section>
    </div>
  </div>

  <footer onclick="window.location.href='{apply_url}'">Apply</footer>
  <script src="/assets/si.js"></script>
</body>
</html>
""")

print(f"\n✅ Job '{role}' added successfully at: {job_path}")

