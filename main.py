import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
import time
from compressor import compress_pdf

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PDFCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("PDF Compressor Premium")
        self.geometry("600x480")
        self.resizable(False, False)
        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        self.input_file = ""
        self.compression_var = ctk.StringVar(value="media")
        
        self.create_widgets()
        
    def create_widgets(self):
        self.label_title = ctk.CTkLabel(self, text="PDF Compressor", font=ctk.CTkFont(size=28, weight="bold"))
        self.label_title.pack(pady=(35, 5))
        
        self.label_subtitle = ctk.CTkLabel(self, text="Transforme arquivo pesado em máxima eficiência livre de problemas", text_color="gray", font=ctk.CTkFont(size=12))
        self.label_subtitle.pack(pady=(0, 25))
        
        self.frame_file = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_file.pack(pady=10, padx=50, fill="x")
        
        self.entry_file = ctk.CTkEntry(self.frame_file, placeholder_text="Nenhum PDF selecionado...", state="disabled", height=35)
        self.entry_file.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.btn_select = ctk.CTkButton(self.frame_file, text="Procurar...", command=self.select_file, width=100, height=35)
        self.btn_select.pack(side="right")
        
        self.label_level = ctk.CTkLabel(self, text="Nível de Compressão (Taxa de Redução):", font=ctk.CTkFont(size=14))
        self.label_level.pack(pady=(25, 10))
        
        self.frame_options = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_options.pack(pady=5)
        
        self.radio_leve = ctk.CTkRadioButton(self.frame_options, text="Leve", variable=self.compression_var, value="leve")
        self.radio_leve.pack(side="left", padx=15)
        
        self.radio_media = ctk.CTkRadioButton(self.frame_options, text="Média", variable=self.compression_var, value="media")
        self.radio_media.pack(side="left", padx=15)
        
        self.radio_alta = ctk.CTkRadioButton(self.frame_options, text="Extrema", variable=self.compression_var, value="extrema")
        self.radio_alta.pack(side="left", padx=15)
        
        self.progressbar = ctk.CTkProgressBar(self, mode="determinate", height=10)
        self.progressbar.set(0)
        
        self.label_status = ctk.CTkLabel(self, text="", text_color="gray", font=ctk.CTkFont(size=12))
        self.label_status.pack(pady=(15, 5))
        
        self.btn_compress = ctk.CTkButton(self, text="COMPRIMIR PDF", command=self.start_compression, height=45, font=ctk.CTkFont(size=15, weight="bold"))
        self.btn_compress.pack(pady=(10, 20), padx=50, fill="x")
        
    def select_file(self):
        filename = filedialog.askopenfilename(
            title="Selecione o PDF",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if filename:
            self.input_file = filename
            self.entry_file.configure(state="normal")
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, self.input_file)
            self.entry_file.configure(state="disabled")
            
            size_mb = os.path.getsize(self.input_file) / (1024 * 1024)
            self.label_status.configure(text=f"Pronto: {size_mb:.2f} MB", text_color="gray")
            
    def start_compression(self):
        if not self.input_file:
            messagebox.showwarning("Aviso", "Selecione um arquivo PDF primeiro clicando em 'Procurar...'.")
            return
            
        level = self.compression_var.get()
        self.btn_compress.configure(state="disabled")
        self.btn_select.configure(state="disabled")
        
        self.progressbar.pack(pady=(0, 10), padx=50, fill="x", before=self.label_status)
        self.progressbar.set(0)
        
        # Reseta o tempo de inicio
        self.start_time = time.time()
        
        self.label_status.configure(text=f"Comprimindo (Modo: {level.capitalize()}) ... Por favor, aguarde.", text_color="#1f6aa5")
        
        threading.Thread(target=self.compress_thread, args=(level,), daemon=True).start()

    def update_progress(self, pct, current, total, eta_str):
        self.progressbar.set(pct)
        lvl_name = self.compression_var.get().capitalize()
        self.label_status.configure(text=f"Processando {lvl_name}: Pág. {current}/{total} | Tempo est.: {eta_str}")

    def compress_thread(self, level):
        try:
            base, ext = os.path.splitext(self.input_file)
            output_file = f"{base}_comprimido{ext}"
            
            # Função de callback pra atualizar a UI
            def on_progress(current, total):
                elapsed = time.time() - self.start_time
                if current > 0 and total > 0:
                    time_per_page = elapsed / current
                    rem_pages = max(0, total - current)
                    eta_seconds = int(time_per_page * rem_pages)
                    mins, secs = divmod(eta_seconds, 60)
                    if mins > 0:
                        eta_str = f"{mins}m {secs}s"
                    else:
                        eta_str = f"{secs}s"
                    pct = current / total
                else:
                    eta_str = "Calculando..."
                    pct = 0.0
                    
                self.after(0, self.update_progress, pct, current, total, eta_str)
            
            compress_pdf(self.input_file, output_file, level, progress_callback=on_progress)
            self.after(0, self.finish_compression, True, output_file)
            
        except Exception as e:
            self.after(0, self.finish_compression, False, str(e))
            
    def finish_compression(self, success, result_file_or_err):
        self.progressbar.pack_forget()
        self.btn_compress.configure(state="normal")
        self.btn_select.configure(state="normal")
        
        if success:
            orig_size = os.path.getsize(self.input_file) / (1024 * 1024)
            new_size = os.path.getsize(result_file_or_err) / (1024 * 1024)
            savings = max(0, 100 - (new_size / orig_size * 100)) if orig_size > 0 else 0
            
            msg = (
                f"Compressão Finalizada!\n\n"
                f"Tamanho Original: {orig_size:.2f} MB\n"
                f"Novo Tamanho: {new_size:.2f} MB\n\n"
                f"(Redução alcançada de {savings:.1f}%)"
            )
            
            self.label_status.configure(text=f"Sucesso: {orig_size:.2f}MB para {new_size:.2f}MB!", text_color="#2eb82e")
            messagebox.showinfo("Sucesso", msg)
        else:
            self.label_status.configure(text="Falha durante a compressão.", text_color="#e62e00")
            messagebox.showerror("Erro Encontrado", result_file_or_err)

if __name__ == "__main__":
    app = PDFCompressorApp()
    app.mainloop()
