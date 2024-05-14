import os
import tkinter as tk
import sys
import time
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DosyaIzleyici(FileSystemEventHandler):
    def __init__(self):
        self.windows = {}

    def dosya_islemi(self, event):
        dosya_adi, dosya_uzantisi = os.path.splitext(event.src_path)
        if os.path.basename(dosya_adi).startswith("~$") or dosya_uzantisi == ".tmp":
            return
        if event.event_type == 'created':
            window = tk.Tk()
            window.title("Dosya Kaydet")
            window.geometry("300x460")
            window.configure(bg='#f0f0f0')

            window.withdraw()
            window.update_idletasks()
            window_width = window.winfo_width()
            window_height = window.winfo_height()
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            window.deiconify()

            window.attributes("-topmost", True)

            window.overrideredirect(True)

            window.configure(borderwidth=4, relief="groove")

            dekantor_label = tk.Label(window, text="DOKÜMANTÖR", font=("Helvetica", 12, "bold"), fg="orange", bg='#f0f0f0')
            dekantor_label.pack(pady=(10, 10))

            top_border = tk.Frame(window, height=2, bd=1, relief=tk.SUNKEN, bg="black")
            top_border.pack(fill=tk.X)

            dosya_etiket = tk.Label(window, text=f"{os.path.basename(event.src_path)}", font=("Helvetica", 8, "italic"), fg="gray", bg='#f2f2f2')
            dosya_etiket.pack(pady=(10, 10), fill=tk.X)

            dosya_etiket.bind("<Configure>", lambda e: dosya_etiket.configure(width=e.width))

            musteri_label = tk.Label(window, text="Müşteri Adı:", font=("Helvetica", 10), anchor='w', bg='#f0f0f0')
            musteri_label.pack(pady=(0, 5), padx=10, anchor='w')
            musteri_entry = tk.Entry(window, width=45, font=("Helvetica", 10))  
            musteri_entry.pack(pady=(0, 5), padx=10, anchor='w')

            devam_label = tk.Label(window, text="Tanım:", font=("Helvetica", 10), anchor='w', bg='#f0f0f0')
            devam_label.pack(pady=(0, 5), padx=10, anchor='w')
            dosya_devam_entry = tk.Entry(window, width=45, font=("Helvetica", 10))  
            dosya_devam_entry.pack(pady=(0, 5), padx=10, anchor='w')

            kaydet_btn = tk.Button(window, width=20, text="Kaydet", command=lambda: self.kaydet(window, event.src_path, dosya_etiket, musteri_entry.get(), dosya_devam_entry.get()))
            kaydet_btn.pack(pady=10, padx=10)

            bottom_border = tk.Frame(window, height=2, bd=1, relief=tk.SUNKEN, bg="black")
            bottom_border.pack(fill=tk.X)

            info_label12 = tk.Label(window, text="ℹ Gerçekten dosyayı doğru yere mi kaydettin?", font=("Helvetica", 8), fg="gray", bg='#f0f0f0')
            info_label12.pack(pady=(5, 0), padx=10, anchor='w')

            info_label1 = tk.Label(window, text="ℹ Dosya ismi boşluk içeremez", font=("Helvetica", 8), fg="gray", bg='#f0f0f0')
            info_label1.pack(pady=(5, 0), padx=10, anchor='w')

            info_label2 = tk.Label(window, text="ℹ Dosya ismi yeniiii, soooon şeklinde kelimeler içeremez", font=("Helvetica", 8), fg="gray", bg='#f0f0f0')
            info_label2.pack(pady=(5, 0), padx=10, anchor='w')

            info_label52 = tk.Label(window, text="ℹ Kaydettiğin dosya ismi server da mevcut mu?", font=("Helvetica", 8), fg="gray", bg='#f0f0f0')
            info_label52.pack(pady=(5, 0), padx=10, anchor='w')

            info_label52_sub = tk.Label(window, text="   - Evet dersen serverdaki dosyanın üzerine kayıt eder.", font=("Helvetica", 8), fg="gray", bg='#f0f0f0')
            info_label52_sub.pack(pady=(0, 0), padx=20, anchor='w')

            info_label5d2_sub = tk.Label(window, text="  - Hayır dersen dosya ismi sonuna V1.. ekler.", font=("Helvetica", 8), fg="gray", bg='#f0f0f0')
            info_label5d2_sub.pack(pady=(0, 0), padx=20, anchor='w')

            info_label5w2 = tk.Label(window, text="ℹ Normal dosya bu müşteri ismine ne gireceğim?", font=("Helvetica", 8), fg="gray", bg='#f0f0f0')
            info_label5w2.pack(pady=(5, 0), padx=10, anchor='w')

            info_label5w2_sub = tk.Label(window, text="    - Müşteri ismine Mitto yazabilirsin.", font=("Helvetica", 8), fg="gray", bg='#f0f0f0')
            info_label5w2_sub.pack(pady=(0, 0), padx=20, anchor='w')
            
            iletişim_etiket = tk.Label(window, text="© İletişim Tasarım Birimi", font=("Helvetica", 8), fg="#6B6B6B", bg='#f0f0f0', anchor="center")
            iletişim_etiket.pack(pady=(5, 0), padx=5, side=tk.BOTTOM, fill=tk.X)

            window.mainloop()

            self.windows[event.src_path] = window

    def kaydet(self, window, file_path, dosya_etiket, musteri_adı, dosya_devam):

       
        if not musteri_adı.strip() or not dosya_devam.strip():
            messagebox.showerror("Hata", "Bir boş bir boşa gel bereber bir boş olalım demiş. Müşteri adı ve dosyanın devamı boş olamaz!")
            return

        if any(char in 'çÇğĞıİöÖşŞüÜ!"#%&\'()*+,-./:;<=>?@[\\]^_`{|}~' for char in musteri_adı+dosya_devam):
            messagebox.showerror("Hata", "Ah hadi amaaa Türkçülüğün tutmuş olabilir ama burada Türkçe harf kullanılmaz.")
            return

        if ' ' in musteri_adı or ' ' in dosya_devam:
            messagebox.showerror("Hata", "Bir boş bir boşa gel bereber bir boş olalım demiş. Müşteri adı veya dosyanın devamında boşluk kullanılamaz!")
            return
        for word in musteri_adı.split() + dosya_devam.split():
            if any(word[i:i+3].lower() == word[i]*3 for i in range(len(word) - 2)):
                messagebox.showerror("Hata", "Hey Hey Hey Orda Durrrrr!! Dosya adında üç ardışık harf içeren kelime kullanılamaz!")
                return
        
        dosya_adi, dosya_uzantisi = os.path.splitext(file_path)

        klasor_yolu = os.path.dirname(dosya_adi)

        yeni_dosya_adi = f"{musteri_adı.capitalize()}_{dosya_devam.capitalize()}{dosya_uzantisi}"

        if os.path.exists(os.path.join(klasor_yolu, yeni_dosya_adi)):
            cevap = messagebox.askquestion("Dikkat Dikkat!! Dosya Zaten Var", f"'{yeni_dosya_adi}' zaten var. Üzerine yazmak istiyor musunuz?")
            if cevap == 'yes':
                os.remove(os.path.join(klasor_yolu, yeni_dosya_adi))
            else:
                sira = 1
                while os.path.exists(os.path.join(klasor_yolu, yeni_dosya_adi)):
                    yeni_dosya_adi = f"{musteri_adı.capitalize()}_{dosya_devam.capitalize()}_v{sira}{dosya_uzantisi}"
                    sira += 1

        hedef_yol = os.path.join(klasor_yolu, yeni_dosya_adi)
        os.rename(file_path, hedef_yol)

        dosya_etiket.config(text=f"Dosya: {os.path.basename(file_path)} -> {yeni_dosya_adi}")

        messagebox.showinfo("Bilgi", f"Dosya {yeni_dosya_adi} olarak kaydedildi.")

        window.destroy()

    def on_created(self, event):
        if os.path.isfile(event.src_path): 
            self.dosya_islemi(event)
        else:
            pass

def hizmeti_baslat():
    izleyici = Observer()
    izleyici.schedule(DosyaIzleyici(), path=r'M:', recursive=True)
    izleyici.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        izleyici.stop()
        izleyici.join()

if __name__ == "__main__":
    hizmeti_baslat()
