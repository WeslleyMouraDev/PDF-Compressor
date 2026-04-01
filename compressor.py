import os
import subprocess
import glob
import re
import math
import time

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

def get_ghostscript_path():
    """Busca o executável do Ghostscript no sistema Windows."""
    paths = [
        r"C:\Program Files\gs\gs*\bin\gswin64c.exe",
        r"C:\Program Files (x86)\gs\gs*\bin\gswin64c.exe",
        r"C:\Program Files\gs\gs*\bin\gswin32c.exe",
        r"C:\Program Files (x86)\gs\gs*\bin\gswin32c.exe"
    ]
    for p in paths:
        matches = glob.glob(p)
        if matches:
            return matches[-1]
    for cmd in ["gswin64c", "gswin32c", "gs"]:
        try:
            process = subprocess.run([cmd, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            if process.returncode == 0:
                return cmd
        except FileNotFoundError:
            pass
    return None

def get_page_count(input_path):
    """Obtém o número de páginas usando PyMuPDF (fitz) de forma instântanea."""
    if fitz:
        try:
            doc = fitz.open(input_path)
            count = doc.page_count
            doc.close()
            return count
        except Exception:
            pass
    return 1

def compress_pdf(input_path, output_path, level="media", progress_callback=None):
    """
    Comprime o PDF utilizando Ghostscript manipulando resoluções de imagens explicitamente.
    Reporta o progresso de página em página através do progress_callback.
    """
    gs_path = get_ghostscript_path()
    if not gs_path:
        raise Exception("O Ghostscript não foi encontrado.\nPor favor, baixe gratuitamente em: https://ghostscript.com/releases/")

    total_pages = get_page_count(input_path)

    base_cmd = [
        gs_path,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dBATCH"
    ]

    # Melhora a compressão forcando downsample nas imagens:
    # Ajustei a Extrema para não perder absolutamente a res (era 72, subi pra 90).
    # Ajustei Media e Leve pra forçar DPI específico (120 e 200).
    
    if level == "extrema":
        base_cmd.extend([
            "-dPDFSETTINGS=/screen", 
            "-dColorImageResolution=90",
            "-dGrayImageResolution=90",
            "-dMonoImageResolution=90"
        ])
    elif level == "media":
        base_cmd.extend([
            "-dPDFSETTINGS=/ebook", 
            "-dColorImageResolution=120",
            "-dGrayImageResolution=120",
            "-dMonoImageResolution=120",
            "-dDownsampleColorImages=true"
        ])
    else: # leve
        base_cmd.extend([
            "-dPDFSETTINGS=/printer",
            "-dColorImageResolution=200",
            "-dGrayImageResolution=200",
            "-dMonoImageResolution=200",
            "-dDownsampleColorImages=true"
        ])
        
    base_cmd.extend([f"-sOutputFile={output_path}", input_path])
    
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    process = subprocess.Popen(
        base_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, # Captura o stderr pro stdout p/ ler "Page 1"
        text=True,
        creationflags=creationflags
    )
    
    page_regex = re.compile(r"Page\s+(\d+)", re.IGNORECASE)
    
    for line in iter(process.stdout.readline, ""):
        if not line:
            break
        match = page_regex.search(line)
        if match and progress_callback:
            try:
                current_page = int(match.group(1))
                progress_callback(current_page, total_pages)
            except ValueError:
                pass

    process.wait()
    if process.returncode != 0:
        raise Exception("O Ghostscript falhou ao comprimir este arquivo.")

    return True
