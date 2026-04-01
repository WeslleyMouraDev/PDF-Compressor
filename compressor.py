import os
import subprocess
import glob

def get_ghostscript_path():
    """
    Busca o executável do Ghostscript no sistema Windows do usuário.
    Tenta localizar em pastas padrões de programas ou através da variável de ambiente PATH.
    """
    paths = [
        r"C:\Program Files\gs\gs*\bin\gswin64c.exe",
        r"C:\Program Files (x86)\gs\gs*\bin\gswin64c.exe",
        r"C:\Program Files\gs\gs*\bin\gswin32c.exe",
        r"C:\Program Files (x86)\gs\gs*\bin\gswin32c.exe"
    ]
    
    for p in paths:
        matches = glob.glob(p)
        if matches:
            return matches[-1]  # Pega a versão mais recente instalada
            
    # Tenta usar diretamente caso o Ghostscript esteja no PATH
    for cmd in ["gswin64c", "gswin32c", "gs"]:
        try:
            # Verifica se está acessível executando um simples check de versão
            process = subprocess.run([cmd, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            if process.returncode == 0:
                return cmd
        except FileNotFoundError:
            pass
            
    return None

def compress_pdf(input_path, output_path, level="media"):
    """
    Comprime o PDF utilizando configurações específicas do Ghostscript para máximo ganho.
    """
    gs_path = get_ghostscript_path()
    if not gs_path:
        raise Exception("O Ghostscript não foi encontrado neste computador.\nÉ obrigatório instalá-lo para que a compressão profunda funcione.\n\nPor favor, faça o download gratuito em: https://ghostscript.com/releases/")

    # Definições de compressão (Ghostscript PDFSETTINGS)
    # /screen - baixa resolução, tela (72 dpi) => Tamanho Muito Pequeno, ideal para visualização
    # /ebook  - média resolução (150 dpi)      => Tamanho Médio, ideal para textos com algumas imagens
    # /printer- alta resolução (300 dpi)       => Tamanho Maior, compressão mínima otimizada
    
    settings = {
        "extrema": "/screen",
        "media": "/ebook",
        "leve": "/printer"
    }
    
    pdfsettings = settings.get(level.lower(), "/ebook")
    
    gs_command = [
        gs_path,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={pdfsettings}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    
    try:
        # Se estivermos no Windows, evita abrir a tela preta (cmd)
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        subprocess.run(gs_command, check=True, creationflags=creationflags)
        return True
    except subprocess.CalledProcessError as e:
        raise Exception(f"Erro inesperado ao comprimir usando Ghostscript:\n{e}")
