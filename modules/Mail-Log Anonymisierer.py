import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import re

# 🌿 Farben & Schrift
BG_COLOR = "#e8f5e9"        # Pastellgrün
ENTRY_BG = "#ffffff"
BTN_BG = "#c8e6c9"
BTN_FG = "#1b5e20"
FONT = ("Segoe UI", 10)

# 🔄 Anonymisierungs-Logik
def anonymize_emails(text):
    email_map = {}

    if email_var.get():
        email_regex = re.compile(r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
        def replace_func(match):
            local, domain = match.group(1), match.group(2)
            full = f"{local}@{domain}"
            if full not in email_map:
                email_map[full] = f"mail{len(email_map) + 1}@{domain}"
            return email_map[full]
        text = email_regex.sub(replace_func, text)

    if host_var.get():
        text = re.sub(r'\b[\w.-]+\.alanod\.intra\b', 'host-intra.alanod.intra', text)
        text = re.sub(r'\b[\w.-]+\.alanod\.de\b', 'host-ext.alanod.de', text)

    if msgid_var.get():
        text = re.sub(r'message-id=<[^@>]+@', 'message-id=<mail1@', text)

    if ip_var.get():
        text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', 'X.X.X.X', text)

    return text

# 🧪 Anonymisierung ausführen
def anonymize_action():
    input_text = input_field.get("1.0", tk.END)
    result = anonymize_emails(input_text)
    output_field.delete("1.0", tk.END)
    output_field.insert(tk.END, result)

# ℹ️ Infofenster anzeigen
def show_info():
    message = (
        "🔐 Dieses Tool anonymisiert technische Logdaten:\n\n"
        "✅ Was kann anonymisiert werden:\n"
        "- Lokalteile von E-Mail-Adressen (z. B. vor dem @)\n"
        "- Interne Hostnamen (*.alanod.intra, *.alanod.de)\n"
        "- Message-ID-Anteile mit E-Mailbezug\n"
        "- Öffentliche IP-Adressen (wenn gewünscht)\n\n"
        "❗ Was bleibt erhalten:\n"
        "- Domains der E-Mail-Adressen (z. B. @alanod.de)\n"
        "- TLS-Verbindungsdetails, externe Servernamen\n\n"
        "📎 Ziel: DSGVO-konforme Logs, die technisch auswertbar bleiben."
    )
    messagebox.showinfo("Was macht dieses Tool?", message)

def save_output():
    content = output_field.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Nichts zu speichern", "Das Ausgabefeld ist leer.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".log",
        filetypes=[("Logdateien", "*.log"), ("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Gespeichert", f"Datei gespeichert:\n{file_path}")

# 🪟 GUI-Aufbau
root = tk.Tk()
root.title("Mail-Log Anonymisierer")
root.configure(bg=BG_COLOR)

# Eingabe-Label + Textfeld
tk.Label(root, text="Log einfügen:", bg=BG_COLOR, font=FONT).pack(anchor='w', padx=10, pady=(10, 0))
input_field = scrolledtext.ScrolledText(root, height=12, width=100, bg=ENTRY_BG, font=FONT)
input_field.pack(padx=10, pady=5)

# 🔘 Optionen: Checkboxen
options_frame = tk.LabelFrame(root, text="Anonymisierungsregeln", bg=BG_COLOR, font=FONT)
options_frame.pack(fill="x", padx=10, pady=(0, 10))

email_var = tk.BooleanVar(value=True)
host_var = tk.BooleanVar(value=True)
msgid_var = tk.BooleanVar(value=True)
ip_var = tk.BooleanVar(value=False)

tk.Checkbutton(options_frame, text="E-Mail-Adressen anonymisieren", variable=email_var,
               bg=BG_COLOR, font=FONT).pack(anchor="w", padx=10)
tk.Checkbutton(options_frame, text="Interne Hostnamen anonymisieren", variable=host_var,
               bg=BG_COLOR, font=FONT).pack(anchor="w", padx=10)
tk.Checkbutton(options_frame, text="Message-ID anonymisieren", variable=msgid_var,
               bg=BG_COLOR, font=FONT).pack(anchor="w", padx=10)
tk.Checkbutton(options_frame, text="Öffentliche IP-Adressen maskieren", variable=ip_var,
               bg=BG_COLOR, font=FONT).pack(anchor="w", padx=10)


# 🔳 Buttonleiste
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Anonymisieren", command=anonymize_action,
          bg=BTN_BG, fg=BTN_FG, font=FONT, relief="raised", padx=10, pady=5).pack(side=tk.LEFT, padx=5)

tk.Button(btn_frame, text="Was macht dieses Tool?", command=show_info,
          bg=BTN_BG, fg=BTN_FG, font=FONT, relief="raised", padx=10, pady=5).pack(side=tk.LEFT, padx=5)

tk.Button(btn_frame, text="Speichern…", command=save_output,
          bg=BTN_BG, fg=BTN_FG, font=FONT, relief="raised", padx=10, pady=5).pack(side=tk.LEFT, padx=5)

# Ausgabe-Label + Textfeld
tk.Label(root, text="Anonymisierter Log:", bg=BG_COLOR, font=FONT).pack(anchor='w', padx=10, pady=(10, 0))
output_field = scrolledtext.ScrolledText(root, height=12, width=100, bg=ENTRY_BG, font=FONT)
output_field.pack(padx=10, pady=(0, 10))

# 🚀 Start
root.mainloop()
