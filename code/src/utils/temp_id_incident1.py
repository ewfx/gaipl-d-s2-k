import pandas as pd

# Load the CSV file
df = pd.read_csv("data/incident_template.csv")  # Replace with your actual file path

# Function to find template_id based on incident_number
def get_template_id(incident_no):
    result = df[df["incident_no"] == incident_no]["job_template_id"]
    return result.iloc[0] if not result.empty else None

# Example usage
incident_no = "INC0029232"  # Replace with the incident number you want to search for
job_template_id = get_template_id(incident_no)

if job_template_id:
    print(f"Template ID for incident {incident_no}: {job_template_id}")
else:
    print(f"No template found for incident {incident_no}")
