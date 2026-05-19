import subprocess
import sys
import os
import time
import webbrowser

def main():

    script_path = os.path.join(
        os.path.dirname(__file__),
        "BD_DMAPLU.py"
    )

    # inicia streamlit
    process = subprocess.Popen([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        script_path,
        "--server.headless=true"
    ])

    # espera alguns segundos para o servidor subir
    time.sleep(3)

    # abre navegador apenas uma vez
    webbrowser.open("http://localhost:8501")

    # mantém processo vivo
    process.wait()

if __name__ == "__main__":
    main()