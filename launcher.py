import subprocess
import sys
import os

def main():
    # Caminho absoluto do arquivo principal
    script_path = os.path.join(os.path.dirname(__file__), "BD_DMAPLU.py")
    
    # Executa o Streamlit chamando o script principal
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", script_path])
    except Exception as e:
        print("Erro ao iniciar o aplicativo Streamlit:", e)

if __name__ == "__main__":
    main()