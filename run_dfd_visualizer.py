import webbrowser
import os
import sys

def main():
    file_path = os.path.abspath("all_dfd_diagrams.html")
    if os.path.exists(file_path):
        print(f"Opening Mermaid DFD Diagrams in Browser: {file_path}")
        webbrowser.open(f"file:///{file_path}")
    else:
        print("Error: all_dfd_diagrams.html not found.")

if __name__ == '__main__':
    main()
