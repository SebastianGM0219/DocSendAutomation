import os
import webbrowser

def open_pdf():
    pdf_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'mcy8h43sjjf5hchf.pdf')
    try:
        webbrowser.open(pdf_path)
        print("Success: File opened successfully")
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    open_pdf()