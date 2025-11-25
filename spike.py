import tkinter as tk
import sys

# --- KONFIGURASI GUI ---
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
CENTER_X = WINDOW_WIDTH // 2
BASE_Y = WINDOW_HEIGHT
LINE_COLOR = "cyan"
# -----------------------

class Animator:
    def __init__(self, master):
        self.master = master
        master.title("Wave & Heartbeat Animator")
        
        self.canvas = tk.Canvas(master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.canvas.pack(pady=10)
        
        self.line = self.canvas.create_line(CENTER_X, BASE_Y, CENTER_X, BASE_Y, fill=LINE_COLOR, width=5)
        
        # Variabel kontrol
        self.is_running = True
        self.current_mode = tk.StringVar(value='GELOMBANG') # Default mode
        self.animation_id = None

        # Variabel state untuk Detak Jantung
        self.heartbeat_steps = [30, 75, 150, 75, 30] # [Base, Half-Peak, Peak, Half-Peak, Base]
        self.heartbeat_index = 0
        
        # Variabel state untuk Gelombang Menelan
        self.wave_length = 10
        self.wave_direction = 1 # 1: Memanjang, -1: Memendek
        self.wave_max = 250
        self.wave_min = 10
        self.wave_step = 10
        self.wave_delay = 30 # ms
        
        # Kontrol GUI
        mode_frame = tk.Frame(master)
        mode_frame.pack()
        
        tk.Radiobutton(mode_frame, text="Gelombang Menelan", variable=self.current_mode, value='GELOMBANG', command=self.reset_animation).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="Detak Jantung", variable=self.current_mode, value='DETAK', command=self.reset_animation).pack(side=tk.LEFT, padx=10)
        
        self.animate_loop()

    def reset_animation(self):
        """Menghentikan animasi lama, mereset state, dan memulai yang baru."""
        if self.animation_id:
            self.master.after_cancel(self.animation_id)
        
        # Reset state
        self.heartbeat_index = 0
        self.wave_length = 10
        self.wave_direction = 1
        
        self.animate_loop()

    def update_line_length(self, length):
        """Memperbarui koordinat garis di Canvas."""
        new_start_y = BASE_Y - length
        self.canvas.coords(self.line, CENTER_X, BASE_Y, CENTER_X, new_start_y)
        
    def animate_loop(self):
        """Fungsi loop utama yang mengarahkan ke mode yang dipilih."""
        mode = self.current_mode.get()
        
        if mode == 'GELOMBANG':
            self.gelombang_menelan()
        elif mode == 'DETAK':
            self.detak_jantung()

    # --- MODE 1: GELOMBANG MENELAN (DIPERBAIKI) ---
    def gelombang_menelan(self):
        
        # Hitung panjang garis baru
        self.wave_length += self.wave_direction * self.wave_step
        
        # Periksa batas dan ubah arah
        if self.wave_length >= self.wave_max:
            self.wave_direction = -1 # Mulai memendek
        elif self.wave_length <= self.wave_min:
            self.wave_direction = 1  # Mulai memanjang
            
        self.update_line_length(self.wave_length)
        
        # Jadwalkan iterasi berikutnya
        self.animation_id = self.master.after(self.wave_delay, self.animate_loop)


    # --- MODE 2: DETAK JANTUNG (DIPERBAIKI) ---
    def detak_jantung(self):
        
        short_delay = 50  # ms untuk pulsa cepat
        long_delay = 400  # ms untuk fase istirahat (diastol)
        base_length = 30
        
        # Fase Sistol (Pulsa Cepat)
        if self.heartbeat_index < len(self.heartbeat_steps):
            length = self.heartbeat_steps[self.heartbeat_index]
            self.update_line_length(length)
            
            self.heartbeat_index += 1
            
            # Jadwalkan langkah berikutnya setelah jeda singkat
            self.animation_id = self.master.after(short_delay, self.animate_loop)
            
        # Fase Diastol (Istirahat)
        else:
            self.update_line_length(base_length) # Pastikan kembali ke dasar
            self.heartbeat_index = 0 # Reset indeks untuk detak berikutnya
            
            # Jadwalkan detak baru setelah jeda panjang
            self.animation_id = self.master.after(long_delay, self.animate_loop)


if __name__ == '__main__':
    root = tk.Tk()
    app = Animator(root)
    
    # Menambahkan penanganan keluar yang rapi
    def on_closing():
        if app.animation_id:
            root.after_cancel(app.animation_id)
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()