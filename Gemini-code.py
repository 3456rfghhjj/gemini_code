import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from google import genai

# Load Gemini API key
API_KEY = os.environ.get("GEMINI_API_KEY", "your_API_key")
client = genai.Client(api_key=API_KEY)

# Colors and fonts
DARK_GREEN_BG = "#2E4A34"
TEXT_COLOR = "#E6F0E8"

CODE_FONT = ("Menlo", 18, "bold")
UI_FONT = (".AppleSystemUIFont", 18, "bold")
LABEL_FONT = (".AppleSystemUIFont", 14, "bold")


def open_file():
  file_path = filedialog.askopenfilename(
      title="Select Python Script",
      filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
  )
  if file_path:
    path_var.set(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
      code_box.delete("1.0", tk.END)
      code_box.insert(tk.END, f.read())


def execute_api_call(prompt):
  try:
    chat = client.chats.create(model="gemini-3.8-flash")
    response = chat.send_message(prompt)
    response_text = response.text

    def update_gui():
      output_box.delete("1.0", tk.END)
      output_box.insert(tk.END, response_text)
      status_label.config(text="Done.")
      submit_btn.config(state=tk.NORMAL)

    root.after(0, update_gui)

  except Exception as e:
    error_text = str(e)

    def show_error():
      messagebox.showerror("API Error", f"An error occurred: {error_text}")
      status_label.config(text="API call failed.")
      submit_btn.config(state=tk.NORMAL)

    root.after(0, show_error)


def send_request():
  code = code_box.get("1.0", tk.END).strip()
  instruction = instruction_entry.get().strip()

  if not code:
    messagebox.showwarning("Error", "Please select or paste some code first!")
    return
  if not instruction:
    messagebox.showwarning(
        "Error", "Please enter what Gemini should do with the code!"
    )
    return

  status_label.config(text="Sending request to Gemini...")
  submit_btn.config(state=tk.DISABLED)

  prompt = (
      "Analyze and modify the following Python code based on the instruction."
      f"\n\nInstruction:\n{instruction}\n\nCode:\n{code}\n\nProvide the"
      " updated code and briefly mention what changed."
  )

  # Run API call in a background thread to prevent UI freezing
  thread = threading.Thread(
      target=execute_api_call, args=(prompt,), daemon=True
  )
  thread.start()


# Main application window
root = tk.Tk()
root.title("Gemini Code Assistant")
root.geometry("1512x1020")

# Top panel: File selection
top_frame = ttk.Frame(root, padding=10)
top_frame.pack(fill=tk.X)

path_var = tk.StringVar()
ttk.Button(top_frame, text="Open .py File", command=open_file).pack(
    side=tk.LEFT, padx=5
)
ttk.Entry(top_frame, textvariable=path_var, font=LABEL_FONT).pack(
    side=tk.LEFT, fill=tk.X, expand=True, padx=5
)

# Input code box
code_frame = ttk.LabelFrame(
    root, text="Original Script Code", padding=(10, 5, 10, 5)
)
code_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
code_box = tk.Text(
    code_frame,
    height=12,
    wrap=tk.NONE,
    font=CODE_FONT,
    bg=DARK_GREEN_BG,
    fg=TEXT_COLOR,
    insertbackground="white",
    relief=tk.FLAT,
    padx=12,
    pady=12,
)
code_box.pack(fill=tk.BOTH, expand=True)

# User task entry and submit button
mid_frame = ttk.Frame(root, padding=10)
mid_frame.pack(fill=tk.X)
ttk.Label(
    mid_frame,
    text="Enter task (e.g., 'fix bugs' or 'add logging'):",
    font=LABEL_FONT,
).pack(anchor=tk.W)
instruction_entry = tk.Entry(
    mid_frame,
    font=UI_FONT,
    bg=DARK_GREEN_BG,
    fg=TEXT_COLOR,
    insertbackground="white",
    relief=tk.FLAT,
)
instruction_entry.pack(fill=tk.X, pady=5, ipady=8)

submit_btn = ttk.Button(
    mid_frame, text="Run with Gemini", command=send_request
)
submit_btn.pack(anchor=tk.E)

# Output code box
output_frame = ttk.LabelFrame(
    root, text="Gemini Response & Refactored Code", padding=(10, 5, 10, 5)
)
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
output_box = tk.Text(
    output_frame,
    height=14,
    wrap=tk.NONE,
    font=CODE_FONT,
    bg=DARK_GREEN_BG,
    fg=TEXT_COLOR,
    insertbackground="white",
    relief=tk.FLAT,
    padx=12,
    pady=12,
)
output_box.pack(fill=tk.BOTH, expand=True)

# Status bar
status_label = ttk.Label(root, text="Ready", font=LABEL_FONT, padding=5)
status_label.pack(anchor=tk.W)

root.mainloop()
