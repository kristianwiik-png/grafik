import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
import os
import json
from PIL import Image, ImageTk


# ---------------- GIT PUSH ----------------
def push_to_github():
    os.system("git add graphic.json")
    os.system('git commit -m "update graphic"')
    os.system("git push")


class Controller:
    def __init__(self, root):
        self.root = root
        self.root.title("KulturCG Controller")

        # DATA
        self.name_var = tk.StringVar(value="Anna Svensson")
        self.title_var = tk.StringVar(value="Projektledare")
        self.logo_path = "logo.png"

        # LOGO CACHE
        self.logo_tk = None

        # UI
        self.build_ui()
        self.build_preview()

        # initial JSON
        self.write_json()

    # ---------------- UI ----------------
    def build_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="x")

        ttk.Label(frame, text="NAMN").pack(anchor="w")
        ttk.Entry(frame, textvariable=self.name_var).pack(fill="x", pady=5)

        ttk.Label(frame, text="TITEL").pack(anchor="w")
        ttk.Entry(frame, textvariable=self.title_var).pack(fill="x", pady=5)

        ttk.Button(frame, text="Välj Logo", command=self.load_logo).pack(fill="x", pady=10)

        ttk.Button(frame, text="Uppdatera Grafik", command=self.write_json).pack(fill="x")

        self.status = ttk.Label(frame, text="")
        self.status.pack(pady=10)

        # live update preview text
        self.name_var.trace_add("write", lambda *args: self.refresh_preview())
        self.title_var.trace_add("write", lambda *args: self.refresh_preview())

    # ---------------- PREVIEW ----------------
    def build_preview(self):
        self.preview_canvas = tk.Canvas(
            self.root,
            width=700,
            height=200,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.preview_canvas.pack(pady=20)

        self.refresh_preview()

    def refresh_preview(self):
        self.preview_canvas.delete("all")

        # LOWER THIRD BACKGROUND
        self.preview_canvas.create_rectangle(
            0, 100, 700, 200,
            fill="#000000",
            outline=""
        )

        # ACCENT BAR
        self.preview_canvas.create_rectangle(
            0, 100, 10, 200,
            fill="#00b3ff",
            outline=""
        )

        # NAME
        self.preview_canvas.create_text(
            25, 135,
            anchor="w",
            text=self.name_var.get(),
            fill="white",
            font=("Arial", 22, "bold")
        )

        # TITLE
        self.preview_canvas.create_text(
            25, 170,
            anchor="w",
            text=self.title_var.get(),
            fill="#bfbfbf",
            font=("Arial", 14)
        )

        # ---------------- LOGO ----------------
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            logo_file = os.path.join(base_dir, self.logo_path)

            img = Image.open(logo_file)
            img = img.resize((80, 80))

            self.logo_tk = ImageTk.PhotoImage(img)

            self.preview_canvas.create_image(
                625, 150,
                image=self.logo_tk
            )

        except Exception as e:
            print("Logo error:", e)

            self.preview_canvas.create_rectangle(
                580, 115, 670, 185,
                fill="#2a2a2a",
                outline=""
            )

            self.preview_canvas.create_text(
                625, 150,
                text="LOGO",
                fill="white",
                font=("Arial", 10)
            )

    # ---------------- LOGO SELECT ----------------
    def load_logo(self):
        file = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file:
            self.logo_path = os.path.basename(file)
            self.write_json()
            self.refresh_preview()

    # ---------------- JSON EXPORT ----------------
    def write_json(self):
        data = {
            "name": self.name_var.get(),
            "title": self.title_var.get(),
            "logo": self.logo_path
        }

        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "graphic.json")

        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            print("✔ JSON uppdaterad:", json_path)
            self.status.config(text="Uppdaterad live ✔")

            # 🔥 PUSH TILL GITHUB
            push_to_github()

        except Exception as e:
            print("❌ JSON error:", e)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app = ttk.Window(themename="darkly")
    Controller(app)
    app.mainloop()