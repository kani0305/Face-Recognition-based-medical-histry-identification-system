import os
import cv2
from tkinter import *
from tkinter import messagebox
from deepface import DeepFace
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database_util import init_db, insert_patient, get_patient_by_name

# Initialize folders and DB
DATA_DIR = "data/registered_faces"
os.makedirs(DATA_DIR, exist_ok=True)
init_db()

# ---- PDF Generation ----
def generate_pdf(patient):
    patient_id, name, age, gender, doctor, bp, history, face_path = patient
    pdf_path = f"data/{name}_report.pdf"

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, 750, "Patient Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Name: {name}")
    c.drawString(100, 680, f"Age: {age}")
    c.drawString(100, 660, f"Gender: {gender}")
    c.drawString(100, 640, f"Doctor: {doctor}")
    c.drawString(100, 620, f"Blood Pressure: {bp}")
    c.drawString(100, 600, f"Medical History: {history}")
    c.drawString(100, 560, f"Face Path: {face_path}")

    c.showPage()
    c.save()
    messagebox.showinfo("PDF Generated", f"Report saved: {pdf_path}")

# ---- Face Capture ----
def capture_face():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    gender = entry_gender.get().strip()
    doctor = entry_doctor.get().strip()
    bp = entry_bp.get().strip()
    history = entry_history.get().strip()

    if not all([name, age, gender, doctor, bp, history]):
        messagebox.showerror("Error", "Please fill all fields before capturing.")
        return

    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Capture Face - Press SPACE to capture / ESC to exit")

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("Capture Face - Press SPACE to capture / ESC to exit", frame)
        k = cv2.waitKey(1)

        if k % 256 == 27:  # ESC
            messagebox.showinfo("Cancelled", "Face capture cancelled.")
            break
        elif k % 256 == 32:  # SPACE
            face_path = os.path.join(DATA_DIR, f"{name}.jpg")
            cv2.imwrite(face_path, frame)
            insert_patient(name, age, gender, doctor, bp, history, face_path)
            messagebox.showinfo("Success", f"Face captured and {name} registered successfully!")
            break

    cam.release()
    cv2.destroyAllWindows()

# ---- Face Recognition ----
def recognize_face():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Recognize Face - Press SPACE to scan / ESC to exit")

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("Recognize Face - Press SPACE to scan / ESC to exit", frame)
        k = cv2.waitKey(1)

        if k % 256 == 27:
            messagebox.showinfo("Cancelled", "Recognition cancelled.")
            break
        elif k % 256 == 32:
            temp_path = "temp.jpg"
            cv2.imwrite(temp_path, frame)

            try:
                result = DeepFace.find(img_path=temp_path, db_path=DATA_DIR, model_name="VGG-Face")
                if len(result[0]) > 0:
                    matched_face_path = result[0].iloc[0]['identity']
                    recognized_name = os.path.splitext(os.path.basename(matched_face_path))[0]
                    patient = get_patient_by_name(recognized_name)

                    if patient:
                        messagebox.showinfo("Recognized", f"Patient record found for {recognized_name}")
                        generate_pdf(patient)
                    else:
                        messagebox.showwarning("Not Found", "Face recognized but no matching patient record found.")
                else:
                    messagebox.showwarning("Not Found", "No matching face found in database.")
            except Exception as e:
                messagebox.showerror("Error", f"Recognition failed: {str(e)}")
            break

    cam.release()
    cv2.destroyAllWindows()

# ---- Quit Program ----
def quit_app():
    root.destroy()

# ---- Tkinter GUI ----
root = Tk()
root.title("Face ID Medical System")
root.geometry("500x550")

Label(root, text="Face ID Medical System", font=("Helvetica", 16, "bold")).pack(pady=10)

Label(root, text="Name").pack()
entry_name = Entry(root)
entry_name.pack()

Label(root, text="Age").pack()
entry_age = Entry(root)
entry_age.pack()

Label(root, text="Gender").pack()
entry_gender = Entry(root)
entry_gender.pack()

Label(root, text="Doctor").pack()
entry_doctor = Entry(root)
entry_doctor.pack()

Label(root, text="Blood Pressure (BP)").pack()
entry_bp = Entry(root)
entry_bp.pack()

Label(root, text="Medical History").pack()
entry_history = Entry(root)
entry_history.pack()

Button(root, text="Register Patient", command=capture_face, bg="lightblue").pack(pady=10)
Button(root, text="Recognize Patient", command=recognize_face, bg="lightgreen").pack(pady=10)
Button(root, text="Quit", command=quit_app, bg="salmon").pack(pady=10)

root.mainloop()
