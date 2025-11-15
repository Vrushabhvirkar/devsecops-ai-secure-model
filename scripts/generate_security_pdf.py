from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        return "No data available."

def main():
    c = canvas.Canvas("Security-Report.pdf", pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Security Report - DevSecOps AI Model")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Generated: {datetime.datetime.now()}")
    y -= 30

    sections = [
        ("Bandit Results", "bandit_output.txt"),
        ("Trivy Filesystem Scan", "trivy_fs.txt"),
        ("Trivy Image Scan", "trivy_img.txt"),
        ("SBOM (CycloneDX)", "sbom.json"),
        ("Gitleaks Scan", "gitleaks.txt"),
    ]

    for title, file in sections:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, title)
        y -= 20

        c.setFont("Helvetica", 10)
        text = read_file(file)
        for line in text.split("\n")[:50]:
            c.drawString(50, y, line[:110])
            y -= 12
            if y < 50:
                c.showPage()
                y = height - 50

        y -= 20

    c.save()

if __name__ == "__main__":
    main()

