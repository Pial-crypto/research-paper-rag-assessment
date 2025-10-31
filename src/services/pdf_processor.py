import PyPDF2
import re

SECTION_KEYWORDS = ["Abstract", "Introduction", "Methods", "Methodology", "Results", "Conclusion"]

def extract_text_with_sections(pdf_path):
    """
    Extracts text from PDF with simple section awareness.
    Also attempts to detect the title from first page.
    Returns: (sections_list, title)
    """
    sections = []
    title = None

    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            # ------------------------
            # TITLE DETECTION
            # ------------------------
            if reader.pages:
                first_page_text = reader.pages[0].extract_text() or ""
                lines = [line.strip() for line in first_page_text.splitlines() if line.strip()]
                title_lines = []
                for line in lines:
                    # stop if a section keyword is found
                    if any(re.search(rf"\b{kw}\b", line, re.IGNORECASE) for kw in SECTION_KEYWORDS):
                        break
                    # skip short lines or just numbers
                    if len(line) < 5 or re.fullmatch(r'^[0-9\-\s]+$', line):
                        continue
                    title_lines.append(line)

                if title_lines:
                    # join first 1-3 lines as best guess
                    title = " ".join(title_lines[:3])
                    title = re.sub(r'\s{2,}', ' ', title).strip()
                    print(f"[DEBUG] Detected Title: {title}")  # <-- print the title here

            # ------------------------
            # SECTION EXTRACTION
            # ------------------------
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                found = False
                for kw in SECTION_KEYWORDS:
                    if re.search(rf"\b{kw}\b", text, re.IGNORECASE):
                        sections.append({"section": kw, "text": text, "page": i+1, "title": title})
                        found = True
                # যদি কোনো keyword না মেলে, fallback page হিসেবে add
                if not found:
                    sections.append({"section": "Other", "text": text, "page": i+1, "title": title})

    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")

    if not sections:
        # fallback: entire text as one section
        try:
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                full_text = "\n".join([p.extract_text() or "" for p in reader.pages])
                sections.append({"section": "FullText", "text": full_text, "page": 1, "title": title})
        except Exception as e:
            print(f"Error reading PDF {pdf_path} in fallback: {e}")

    return sections, title
