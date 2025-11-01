import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from PIL import Image

REPORT_DIR = "data/reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def generate_patient_report(patient_data, face_image_path):
    """
    patient_data: dict containing patient info
    face_image_path: path to recognized face image
    """
    filename = f"{patient_data['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = os.path.join(REPORT_DIR, filename)

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, 750, "🩺 Patient Medical Report")

    c.setFont("Helvetica", 12)
    y = 700
    for key, value in patient_data.items():
        c.drawString(80, y, f"{key.capitalize()}: {value}")
        y -= 20

    c.drawString(80, y - 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Add face image to the report if exists
    if os.path.exists(face_image_path):
        try:
            img = Image.open(face_image_path)
            img.thumbnail((150, 150))
            img.save("temp_face.jpg")
            c.drawImage("temp_face.jpg", 400, 600, width=120, height=120)
            os.remove("temp_face.jpg")
        except Exception as e:
            print("Error adding image:", e)

    c.save()
    print(f"✅ Report saved as {pdf_path}")
    return pdf_path
