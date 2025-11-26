from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def generate_pdf(result_id: str, text: str, prediction: str, score: float, save_path: str):
    c = canvas.Canvas(save_path, pagesize=A4)
    c.setFont("Helvetica", 12)

    c.drawString(50, 800, f"Hasil Analisis")
    c.drawString(50, 780, f"ID: {result_id}")
    c.drawString(50, 760, f"Label Prediksi: {prediction}")
    c.drawString(50, 740, f"Akurasi: {score}")

    c.drawString(50, 700, "Teks Analisis:")
    text_lines = text.split("\n")

    y = 680
    for line in text_lines:
        if y < 50:
            c.showPage()
            y = 800
        c.drawString(50, y, line)
        y -= 20

    c.save()
