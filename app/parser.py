import pdfplumber
import re

def parse_pdf(pdf_path):

    rows = []

    with pdfplumber.open(pdf_path) as pdf:

        text = "\n".join(
            page.extract_text() or ""
            for page in pdf.pages
        )

    for line in text.splitlines():

        if not re.match(r"^\d+\s+\d{7}", line):
            continue

        parts = line.split()

        employee_id = parts[1]

        # dmd_index = parts.index("DMD")

        # employee_name = " ".join(parts[2:dmd_index])

        # department = "DMD"
        
        department_index = None

        for i in range(2, len(parts)):
            if re.match(r"\d{2}/\d{2}/\d{4}", parts[i]):
                department_index = i - 1
                break

        if department_index is None:
            continue

        employee_name = " ".join(parts[2:department_index])

        department = parts[department_index]

        date = parts[department_index + 1]
        day = parts[department_index + 2]

        remain = parts[department_index + 3:]

        check_in = ""
        check_out = ""
        shift = ""

        if len(remain) == 1:
            shift = remain[0]

        elif len(remain) == 2:
            check_in = remain[0]
            shift = remain[1]

        elif len(remain) >= 3:
            check_in = remain[0]
            check_out = remain[1]
            shift = remain[2]

        rows.append({
            "employee_id": employee_id,
            "employee_name": employee_name,
            "department": department,
            "date": date,
            "day": day,
            "check_in": check_in,
            "check_out": check_out,
            "shift": shift
        })

    return rows