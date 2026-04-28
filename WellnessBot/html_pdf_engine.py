import os
import tempfile
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

def create_premium_pdf(data: dict, output_path: str):
    """
    Renders the data into an HTML template using Jinja2,
    then uses Playwright to generate a print-perfect PDF.
    """
    # 1. Setup Jinja env
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(("html", "xml")),
    )
    template = env.get_template('dossier_layout.html')
    
    # 2. Render HTML string
    html_content = template.render(**data)
    
    # Optional: Save for debugging
    # with open("debug_render.html", "w", encoding="utf-8") as f:
    #     f.write(html_content)
    
    # 3. Use Playwright to print to PDF
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Load the HTML content directly
        page.set_content(html_content, wait_until="domcontentloaded")
        page.wait_for_timeout(400)
        
        # Generate PDF with precise A4 dimensions, no margins (handled via CSS padding)
        page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
        )
        
        browser.close()
        
    return output_path

if __name__ == "__main__":
    import test_data
    output_file = r"C:\Users\HP\Desktop\PREMIUM_DOSSIER_V2.pdf"
    print("Engine Starting... (Generating Premium PDF)")
    create_premium_pdf(test_data.DUMMY_DATA, output_file)
    print(f"Generated successfully: {output_file}")
