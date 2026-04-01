import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from compressor import compress_pdf

# Configuração Base do CustomTkinter (Dark Mode Premium)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PDFCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração da Janela
        self.title("PDF Compressor Premium")
        self.geometry("600x450")
        self.resizable(False, False)
        
        # Centralizando a janela no monitor
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Variáveis de Estado
        self.input_file = ""
        self.compression_var = ctk.StringVar(value="media")
        
        # Construção da UI Principal
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        self.label_title = ctk.CTkLabel(self, text="PDF Compressor", font=ctk.CTkFont(size=28, weight="bold"))
        self.label_title.pack(pady=(35, 5))
        
        self.label_subtitle = ctk.CTkLabel(self, text="Transforme alto peso em máxima eficiência", text_color="gray", font=ctk.CTkFont(size=13))
        self.label_subtitle.pack(pady=(0, 25))
        
        # Área de Arquivo
        self.frame_file = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_file.pack(pady=10, padx=50, fill="x")
        
        self.entry_file = ctk.CTkEntry(self.frame_file, placeholder_text="Nenhum PDF selecionado...", state="disabled", height=35)
        self.entry_file.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.btn_select = ctk.CTkButton(self.frame_file, text="Procurar...", command=self.select_file, width=100, height=35)
        self.btn_select.pack(side="right")
        
        # Opções de Compressão
        self.label_level = ctk.CTkLabel(self, text="Nível de Compressão (Taxa de Redução):", font=ctk.CTkFont(size=14))
        self.label_level.pack(pady=(25, 10))
        
        self.frame_options = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_options.pack(pady=5)
        
        # RadioButtons alinhados horizontalmente
        self.radio_leve = ctk.CTkRadioButton(self.frame_options, text="Leve", variable=self.compression_var, value="leve")
        self.radio_leve.pack(side="left", padx=15)
        
        self.radio_media = ctk.CTkRadioButton(self.frame_options, text="Média", variable=self.compression_var, value="media")
        self.radio_media.pack(side="left", padx=15)
        
        self.radio_alta = ctk.CTkRadioButton(self.frame_options, text="Extrema", variable=self.compression_var, value="extrema")
        self.radio_alta.pack(side="left", padx=15)
        
        # Barra e Status de Progresso (Visíveis apenas durante execução)
        self.progressbar = ctk.CTkProgressBar(self, mode="indeterminate", height=10)
        self.progressbar.set(0)
        
        self.label_status = ctk.CTkLabel(self, text="", text_color="gray", font=ctk.CTkFont(size=12))
        self.label_status.pack(pady=(15, 5))
        
        # Botão Principal (Comprimir)
        self.btn_compress = ctk.CTkButton(self, text="COMPRIMIR PDF", command=self.start_compression, height=45, font=ctk.CTkFont(size=15, weight="bold"))
        self.btn_compress.pack(pady=(10, 20), padx=50, fill="x")
        
    def select_file(self):
        filename = filedialog.askopenfilename(
            title="Selecione o PDF",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if filename:
            self.input_file = filename
            
            # Atualiza campo visual
            self.entry_file.configure(state="normal")
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, self.input_file)
            self.entry_file.configure(state="disabled")
            
            # Atualiza status com o tamanho do arquivo
            size_mb = os.path.getsize(self.input_file) / (1024 * 1024)
            self.label_status.configure(text=f"Pronto: {size_mb:.2f} MB", text_color="gray")
            
    def start_compression(self):
        if not self.input_file:
            messagebox.showwarning("Aviso", "Por favor, selecione um arquivo PDF primeiro clicando em 'Procurar...'.")
            return
            
        level = self.compression_var.get()
        
        # Trava UI para não permitir re-cliques
        self.btn_compress.configure(state="disabled")
        self.btn_select.configure(state="disabled")
        
        # Exibe progresso
        self.progressbar.pack(pady=(0, 10), padx=50, fill="x", before=self.label_status)
        self.progressbar.start()
        
        # Altera estado visual do texto
        self.label_status.configure(text=f"Comprimindo (Modo: {level.capitalize()}) ... Por favor, aguarde.", text_color="#1f6aa5")
        
        # Executa em Thread separada para não congelar o Tkinter
        threading.Thread(target=self.compress_thread, args=(level,), daemon=True).start()
        
    def compress_thread(self, level):
        try:
            base, ext = os.path.splitext(self.input_file)
            output_file = f"{base}_comprimido{ext}"
            
            # Chama o compressor real (Ghostscript)
            compress_pdf(self.input_file, output_file, level)
            
            # Calcula tamanhos após a compressão
            orig_size = os.path.getsize(self.input_file) / (1024 * 1024)
            new_size = os.path.getsize(output_file) / (1024 * 1024)
            savings = 100 - (new_size / orig_size * 100) if orig_size > 0 else 0
            
            msg = (
                f"Compressão Efetuada!\n\n"
                f"Tamanho Original: {orig_size:.2f} MB\n"
                f"Novo Tamanho: {new_size:.2f} MB\n\n"
                f"(Redução alcançada de {savings:.1f}%)"
            )
            
            # Retorna para a thread principal (UI) para atualizar com sucesso
            self.after(0, self.finish_compression, True, msg)
            
        except Exception as e:
            # Retorna para a thread principal com erro
            self.after(0, self.finish_compression, False, str(e))
            
    def finish_compression(self, success, message):
        # Reseta e oculta a barra de progresso
        self.progressbar.stop()
        self.progressbar.pack_forget()
        
        # Libera controles
        self.btn_compress.configure(state="normal")
        self.btn_select.configure(state="normal")
        
        if success:
            self.label_status.configure(text="Concluído com enorme sucesso!", text_color="#2eb82e")
            messagebox.showinfo("Sucesso", message)
        else:
            self.label_status.configure(text="Falha durante a compressão.", text_color="#e62e00")
            messagebox.showerror("Erro de Dependência ou Sistema", message)

if __name__ == "__main__":
    app = PDFCompressorApp()
    app.mainloop()
