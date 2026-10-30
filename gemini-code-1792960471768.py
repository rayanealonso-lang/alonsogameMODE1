import os
import zipfile
import customtkinter as ctk
from tkinter import filedialog, messagebox

# تحديد مجلد حفظ الألعاب في حاسوبك بصورة مستقلة ومستقرة
GAMES_STORE_DIR = os.path.join(os.path.expanduser("~"), "PlayStationGameHub")
os.makedirs(GAMES_STORE_DIR, exist_ok=True)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class PlayStationHubApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PLAYSTATION GAME HUB")
        self.geometry("750x500")
        self.resizable(False, False)
        self.selected_game = None

        # رأس التطبيق بستايل بلايستيشن الفخم
        header = ctk.CTkFrame(self, fg_color="#16161D", corner_radius=0, height=60)
        header.pack(fill="x", side="top")
        title = ctk.CTkLabel(header, text="🎮 PLAYSTATION GAME HUB", font=ctk.CTkFont(size=20, weight="bold"), text_color="#FF3333")
        title.pack(pady=15, padx=20, anchor="w")

        # الجسم الأساسي
        body = ctk.CTkFrame(self, fg_color="#0F0F12")
        body.pack(fill="both", expand=True, padx=20, pady=20)

        lbl_info = ctk.CTkLabel(body, text="مكتبة الألعاب الخاصة بك (اختر لعبة للتشغيل):", text_color="#BBBBBB", font=ctk.CTkFont(size=14))
        lbl_info.pack(anchor="w", pady=(0, 5))

        # إطار الألعاب
        self.games_frame = ctk.CTkScrollableFrame(body, fg_color="#16161D", border_color="#2B2B36", border_width=1, corner_radius=10, height=250)
        self.games_frame.pack(fill="both", expand=True, pady=5)
        self.load_installed_games()

        # أزرار التحكم
        btn_frame = ctk.CTkFrame(body, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(15, 0))

        btn_add = ctk.CTkButton(btn_frame, text="➕ إضافة لعبة جديدة (.zip)", fg_color="#8B0000", hover_color="#A00000", font=ctk.CTkFont(size=14, weight="bold"), height=42, command=self.add_game)
        btn_add.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_launch = ctk.CTkButton(btn_frame, text="▶ تشغيل اللعبة المختارة", fg_color="#1F1F2B", border_color="#8B0000", border_width=1, hover_color="#2B2B36", font=ctk.CTkFont(size=14, weight="bold"), height=42, command=self.launch_game)
        btn_launch.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # شريط الحالة
        self.status_label = ctk.CTkLabel(body, text="الحالة: جاهز للعمل بدون إنترنت", text_color="#888888", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=(10, 0))

    def load_installed_games(self):
        for widget in self.games_frame.winfo_children():
            widget.destroy()
        
        if os.path.exists(GAMES_STORE_DIR):
            games = [d for d in os.listdir(GAMES_STORE_DIR) if os.path.isdir(os.path.join(GAMES_STORE_DIR, d))]
            if games:
                for game in games:
                    btn = ctk.CTkButton(self.games_frame, text=f"🎮  {game}", fg_color="#1F1F2B", hover_color="#8B0000", anchor="w", font=ctk.CTkFont(size=14), height=40, command=lambda g=game: self.select_game(g))
                    btn.pack(fill="x", pady=4, padx=5)
            else:
                lbl = ctk.CTkLabel(self.games_frame, text="لا توجد ألعاب مضافة بعد.", text_color="#777777")
                lbl.pack(pady=20)

    def select_game(self, game_name):
        self.selected_game = game_name
        self.status_label.configure(text=f"اللعبة المحددة: {game_name}")

    def add_game(self):
        file_path = filedialog.askopenfilename(title="اختر ملف اللعبة المضغوط", filetypes=[("Zip Files", "*.zip")])
        if file_path:
            self.status_label.configure(text="جاري معالجة اللعبة...")
            self.update()
            try:
                game_name = os.path.splitext(os.path.basename(file_path))[0]
                target_dir = os.path.join(GAMES_STORE_DIR, game_name)
                os.makedirs(target_dir, exist_ok=True)

                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)

                for root, _, files in os.walk(target_dir):
                    for f in files:
                        fp = os.path.join(root, f)
                        try:
                            if os.path.getsize(fp) == 0:
                                os.remove(fp)
                        except Exception:
                            pass

                self.status_label.configure(text="تمت إضافة اللعبة بنجاح!")
                self.load_installed_games()
                messagebox.showinfo("PlayStation Hub", f"تمت إضافة اللعبة بنجاح:\n{game_name}")
            except Exception as e:
                messagebox.showerror("خطأ", f"تعذر معالجة اللعبة:\n{str(e)}")

    def launch_game(self):
        if not self.selected_game:
            messagebox.showwarning("تنبيه", "الرجاء النقر على أي لعبة من القائمة لتحديدها أولاً!")
            return
        game_dir = os.path.join(GAMES_STORE_DIR, self.selected_game)
        exe_files = []
        for root, _, files in os.walk(game_dir):
            for f in files:
                if f.endswith(".exe"):
                    exe_files.append(os.path.join(root, f))
        if exe_files:
            try:
                os.startfile(exe_files[0])
                self.status_label.configure(text=f"جاري تشغيل: {self.selected_game}")
            except Exception as e:
                messagebox.showerror("خطأ", f"تعذر تشغيل ملف الـ EXE:\n{str(e)}")
        else:
            messagebox.showwarning("تنبيه", "لم يتم العثور على ملف تشغيل (.exe) داخل مجلد هذه اللعبة.")

if __name__ == "__main__":
    app = PlayStationHubApp()
    app.mainloop()