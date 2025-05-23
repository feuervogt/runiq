import tkinter as tk
from tkinter import ttk
import subprocess
import os

SCRIPT_DIR = os.path.join(os.path.dirname(__file__), '..', 'modules')

STYLE_MAP = {
    '.py':   {'color': '#10B981', 'tooltip': 'Python-Skript 🐍'},
    '.sh':   {'color': '#3B82F6', 'tooltip': 'Shell-Skript 🐚'},
    '.ps1':  {'color': '#6366F1', 'tooltip': 'PowerShell 🪟'},
    '.bat':  {'color': '#F97316', 'tooltip': 'Batch-Datei 🧱'},
}

# Farbdefinitionen
LIGHT_BUTTON_BG = "#D3D3D3"
LIGHT_BUTTON_FG = "#000000"
LIGHT_BUTTON_ACTIVE = "#B0B0B0"

LIGHT_ACTION_BG = "#005C4B"
LIGHT_ACTION_FG = "#FFFFFF"
LIGHT_ACTION_ACTIVE = "#004238"

DARK_BUTTON_BG = "#4B5563"
DARK_BUTTON_FG = "#F9FAFB"
DARK_BUTTON_ACTIVE = "#6B7280"

DARK_ACTION_BG = "#047857"
DARK_ACTION_FG = "#F9FAFB"
DARK_ACTION_ACTIVE = "#065F46"

BUTTON_BORDER = "#808080"

class RuniqApp:
    def __init__(self, root):
        self.root = root
        self.dark_mode = False
        self.colors = {}
        self.buttons = []
        self.init_styles()
        self.setup_ui()

    def init_styles(self):
        self.update_theme()

    def update_theme(self):
        if self.dark_mode:
            self.colors = {
                "bg": "#1F2937",
                "fg": "#FACC15",
                "text_bg": "#111827",
                "text_fg": "#F9FAFB",
                "button_bg": DARK_BUTTON_BG,
                "button_fg": DARK_BUTTON_FG,
                "button_active": DARK_BUTTON_ACTIVE,
                "action_bg": DARK_ACTION_BG,
                "action_fg": DARK_ACTION_FG,
                "action_active": DARK_ACTION_ACTIVE,
                "font": ("Consolas", 10),
                "stdout": "#10B981",
                "stderr": "#EF4444",
            }
        else:
            self.colors = {
                "bg": "#F3F4F6",
                "fg": "#111827",
                "text_bg": "#F9FAFB",
                "text_fg": "#1F2937",
                "button_bg": LIGHT_BUTTON_BG,
                "button_fg": LIGHT_BUTTON_FG,
                "button_active": LIGHT_BUTTON_ACTIVE,
                "action_bg": LIGHT_ACTION_BG,
                "action_fg": LIGHT_ACTION_FG,
                "action_active": LIGHT_ACTION_ACTIVE,
                "font": ("Consolas", 10),
                "stdout": "#10B981",
                "stderr": "#EF4444",
            }
        self.root.configure(bg=self.colors["bg"])

    def run_script(self, script_name):
        ext = os.path.splitext(script_name)[1]
        script_path = os.path.join(SCRIPT_DIR, script_name)

        if ext == '.py':
            cmd = ['python', script_path]
        elif ext == '.sh':
            cmd = ['bash', script_path]
        elif ext == '.ps1':
            cmd = ['powershell', '-ExecutionPolicy', 'Bypass', '-File', script_path]
        elif ext == '.bat':
            cmd = [script_path]
        else:
            self.write_output("Nicht unterst\u00fctzter Dateityp.", is_error=True)
            return

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.output_text.configure(state="normal")
            self.output_text.delete(1.0, tk.END)
            self.write_output(f"$ {script_name}\n", style="header")
            if result.stdout:
                self.write_output(result.stdout, style="stdout")
            if result.stderr:
                self.write_output(result.stderr, style="stderr")
            if not result.stdout and not result.stderr:
                self.write_output("(kein Output)", style="stdout")
            self.output_text.configure(padx=10, pady=4)
        except Exception as e:
            self.write_output(str(e), style="stderr")

    def write_output(self, text, style="stdout", is_error=False):
        tag = style if style in self.output_text.tag_names() else "stdout"
        self.output_text.insert(tk.END, text, tag)
        self.output_text.see(tk.END)

    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()
        self.refresh_ui()

    def refresh_ui(self):
        self.root.configure(bg=self.colors["bg"])
        self.title.configure(background=self.colors["bg"], foreground=self.colors["fg"])
        self.output_label.configure(background=self.colors["bg"], foreground=self.colors["fg"])
        self.output_text.configure(bg=self.colors["text_bg"], fg=self.colors["text_fg"], insertbackground=self.colors["text_fg"])
        self.search_label.configure(background=self.colors["bg"], foreground=self.colors["fg"])

        self.toggle_button.configure(
            bg=self.colors["action_bg"],
            fg=self.colors["action_fg"],
            activebackground=self.colors["action_active"]
        )

        for name, btn, ext in self.buttons:
            btn.configure(
                bg=self.colors["button_bg"],
                fg=self.colors["button_fg"],
                activebackground=self.colors["button_active"]
            )

    def setup_ui(self):
        self.root.title("Runiq – Script Launcher")
        self.root.geometry("720x860")
        self.root.resizable(False, False)

        self.title = ttk.Label(self.root, text="Verf\u00fcgbare Skripte", font=("Segoe UI", 14, "bold"))
        self.title.pack(pady=10)

        self.toggle_button = tk.Button(
            self.root, text="🌃 Dark Mode", command=self.toggle_mode,
            bg=self.colors["action_bg"], fg=self.colors["action_fg"],
            activebackground=self.colors["action_active"],
            relief="raised", bd=2,
            font=("Segoe UI", 10, "bold"),
            padx=8, pady=4
        )
        self.toggle_button.pack(anchor="ne", padx=10)

        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=(0, 10), anchor='w')

        self.search_label = ttk.Label(search_frame, text="🔍 Suche:", font=("Segoe UI", 10, "bold"))
        self.search_label.pack(side="left", padx=5)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.apply_filter())

        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40,
                                font=("Segoe UI", 10), relief="solid")
        search_entry.pack(side="left", padx=5)

        legend_frame = ttk.Frame(self.root)
        legend_frame.pack(pady=(0, 5), fill="x")

        self.active_filter = None
        for ext, props in STYLE_MAP.items():
            legend = tk.Label(legend_frame,
                              text=props['tooltip'] + " (Filter)",
                              bg=props['color'],
                              fg="white",
                              font=("Segoe UI", 10, "bold"),
                              relief="raised",
                              bd=2,
                              padx=6,
                              pady=4)
            legend.pack(side="left", padx=5, pady=5)
            legend.bind("<Button-1>", lambda e, ext=ext, lbl=legend: self.filter_by_type(ext, lbl))

        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(pady=5, fill='x')

        scripts_by_type = self.list_scripts_grouped()
        for ext in sorted(STYLE_MAP):
            scripts = scripts_by_type.get(ext, [])
            for script in sorted(scripts):
                script_name = os.path.splitext(script)[0]
                btn = tk.Button(container,
                                text=script_name,
                                width=50,
                                bg=self.colors["button_bg"],
                                fg=self.colors["button_fg"],
                                activebackground=self.colors["button_active"],
                                relief="raised",
                                bd=2,
                                font=("Segoe UI", 10),
                                highlightbackground=BUTTON_BORDER,
                                command=lambda s=script: self.run_script(s))
                btn.pack(pady=2)
                self.create_tooltip(btn, STYLE_MAP[ext]['tooltip'])
                self.buttons.append((script_name.lower(), btn, ext))

        self.output_label = ttk.Label(self.root, text="Skript-Ausgabe", font=("Segoe UI", 12, "bold"))
        self.output_label.pack(pady=(10, 0))

        output_frame = ttk.Frame(self.root)
        output_frame.pack(pady=5, fill='both', expand=True)

        self.output_text = tk.Text(output_frame, wrap="word", height=15,
                                   bg=self.colors["text_bg"],
                                   fg=self.colors["text_fg"],
                                   insertbackground=self.colors["text_fg"],
                                   font=self.colors["font"],
                                   relief="flat")
        self.output_text.pack(side="left", fill="both", expand=True)
        self.output_text.configure(state="disabled")

        scroll = ttk.Scrollbar(output_frame, command=self.output_text.yview)
        scroll.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=scroll.set)

        self.output_text.tag_configure("stdout", foreground=self.colors["stdout"])
        self.output_text.tag_configure("stderr", foreground=self.colors["stderr"])
        self.output_text.tag_configure("header", foreground=self.colors["fg"], font=("Consolas", 10, "bold"))

        self.refresh_ui()

    def apply_filter(self):
        query = self.search_var.get().lower().strip()
        for name, btn, ext in self.buttons:
            is_visible = query in name
            if self.active_filter and ext != self.active_filter:
                is_visible = False
            btn.pack(pady=2) if is_visible else btn.pack_forget()

    def filter_by_type(self, ext, label):
        if self.active_filter == ext:
            self.active_filter = None
            label.config(relief="raised", bd=2)
        else:
            self.active_filter = ext
            for widget in label.master.winfo_children():
                widget.config(relief="raised", bd=2)
            label.config(relief="sunken", bd=3)
        self.apply_filter()

    def list_scripts_grouped(self):
        allowed = STYLE_MAP.keys()
        files = [f for f in os.listdir(SCRIPT_DIR) if f.endswith(tuple(allowed))]
        grouped = {}
        for file in files:
            ext = os.path.splitext(file)[1]
            grouped.setdefault(ext, []).append(file)
        return grouped

    def create_tooltip(self, widget, text):
        tip = tk.Toplevel(widget)
        tip.withdraw()
        tip.overrideredirect(True)
        tip_label = tk.Label(tip, text=text, background="#FACC15", relief="solid", borderwidth=1,
                             font=("Segoe UI", 9), padx=4, pady=2)
        tip_label.pack()

        def enter(event):
            x, y = event.x_root + 10, event.y_root + 10
            tip.geometry(f"+{x}+{y}")
            tip.deiconify()

        def leave(event):
            tip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

if __name__ == "__main__":
    root = tk.Tk()
    app = RuniqApp(root)
    root.mainloop()
