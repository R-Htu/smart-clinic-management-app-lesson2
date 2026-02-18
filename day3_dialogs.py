# ============================================================
#  DAY 3 — Dialogs (Add Patient & Add Appointment)
#  Smart Clinic Management System
#  Topics: tk.Toplevel, tk.StringVar, tk.OptionMenu,
#          form validation, messagebox, collecting form data
#  (builds on Day 1 + Day 2)
# ============================================================

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

COLORS = {
    'bg':      '#f0f4f8',
    'sidebar': '#1a2340',
    'card':    '#ffffff',
    'text':    '#1e2d40',
    'muted':   '#8a99b0',
    'accent':  '#4f7ef8',
    'green':   '#2ec87a',
    'border':  '#dde3ef',
    'error':   '#e74c3c',
}

FONTS = {
    'title':   ('Segoe UI', 14, 'bold'),
    'heading': ('Segoe UI', 12, 'bold'),
    'normal':  ('Segoe UI', 11),
    'small':   ('Segoe UI', 9),
    'btn':     ('Segoe UI', 10, 'bold'),
    'label':   ('Segoe UI', 10),
}


# ── Reusable helpers ─────────────────────────────────────────

def make_button(parent, text, color, command, width=160):
    """Rounded canvas button (same as Day 2)"""
    W, H, R = width, 36, 8
    canvas = tk.Canvas(parent, width=W, height=H,
                        bg=COLORS['card'], highlightthickness=0, cursor='hand2')

    def draw(c):
        canvas.delete('all')
        canvas.create_arc(0,     0,     R*2,   R*2,   start=90,  extent=90, fill=c, outline=c)
        canvas.create_arc(W-R*2, 0,     W,     R*2,   start=0,   extent=90, fill=c, outline=c)
        canvas.create_arc(0,     H-R*2, R*2,   H,     start=180, extent=90, fill=c, outline=c)
        canvas.create_arc(W-R*2, H-R*2, W,     H,     start=270, extent=90, fill=c, outline=c)
        canvas.create_rectangle(R, 0, W-R, H, fill=c, outline=c)
        canvas.create_rectangle(0, R, W, H-R, fill=c, outline=c)
        canvas.create_text(W//2, H//2, text=text, fill='white', font=FONTS['btn'])

    def darken(h, a=25):
        return '#{:02x}{:02x}{:02x}'.format(
            max(0, int(h[1:3],16)-a),
            max(0, int(h[3:5],16)-a),
            max(0, int(h[5:7],16)-a))

    draw(color)
    canvas.bind('<Enter>',    lambda e: draw(darken(color)))
    canvas.bind('<Leave>',    lambda e: draw(color))
    canvas.bind('<Button-1>', lambda e: command())
    return canvas

def labeled_entry(parent, label_text, row, required=False):
    """
    Creates a label + entry pair inside a grid layout.
    Returns the Entry widget so we can read its value later.
    """
    lbl = tk.Label(parent, font=FONTS['label'], bg=COLORS['card'],
                   fg=COLORS['text'],
                   text=label_text + (' *' if required else ''))
    lbl.grid(row=row, column=0, sticky='w', padx=(24, 12), pady=(10, 0))

    entry_frame = tk.Frame(parent, bg=COLORS['border'], pady=1, padx=1)
    entry_frame.grid(row=row, column=1, sticky='ew', padx=(0, 24), pady=(10, 0))

    entry = tk.Entry(entry_frame, font=FONTS['normal'], relief=tk.FLAT,
                     bg=COLORS['card'], fg=COLORS['text'],
                     insertbackground=COLORS['accent'])
    entry.pack(fill=tk.BOTH, ipady=6, padx=6)

    # Highlight border on focus
    entry.bind('<FocusIn>',  lambda e: entry_frame.config(bg=COLORS['accent']))
    entry.bind('<FocusOut>', lambda e: entry_frame.config(bg=COLORS['border']))

    return entry


# ─────────────────────────────────────────────────────────────
#  DIALOG 1: Add Patient
# ─────────────────────────────────────────────────────────────

def open_patient_dialog(parent, on_save=None):
    """
    Opens a Toplevel window (a popup) with a patient form.
    tk.Toplevel = a secondary window that belongs to the parent.
    """

    # ── Create the popup window ──────────────────────────────
    dialog = tk.Toplevel(parent)
    dialog.title("Add New Patient")
    dialog.geometry("480x460")
    dialog.config(bg=COLORS['card'])
    dialog.resizable(False, False)

    # Keep dialog on top of the main window
    dialog.transient(parent)
    dialog.grab_set()            # block clicks on main window while open

    # ── Header ───────────────────────────────────────────────
    header = tk.Frame(dialog, bg=COLORS['accent'], height=54)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    tk.Label(header, text="👤  Add New Patient", font=FONTS['heading'],
             fg='white', bg=COLORS['accent']).pack(side=tk.LEFT, padx=20, pady=14)

    # ── Form area ────────────────────────────────────────────
    form = tk.Frame(dialog, bg=COLORS['card'])
    form.pack(fill=tk.BOTH, expand=True)
    form.columnconfigure(1, weight=1)   # column 1 stretches

    # Form fields — each returns an Entry widget
    name_entry  = labeled_entry(form, "Full Name",    row=0, required=True)
    age_entry   = labeled_entry(form, "Age",          row=1, required=True)
    phone_entry = labeled_entry(form, "Phone",        row=2)
    email_entry = labeled_entry(form, "Email",        row=3)

    # Gender — use OptionMenu (a dropdown) instead of Entry
    tk.Label(form, text="Gender", font=FONTS['label'],
             bg=COLORS['card'], fg=COLORS['text']).grid(
                 row=4, column=0, sticky='w', padx=(24, 12), pady=(10, 0))

    gender_var = tk.StringVar(value='Select')     # StringVar holds the selected value
    gender_menu = tk.OptionMenu(form, gender_var, 'Male', 'Female', 'Other')
    gender_menu.config(font=FONTS['normal'], bg=COLORS['card'],
                       relief=tk.FLAT, highlightthickness=1,
                       highlightbackground=COLORS['border'])
    gender_menu.grid(row=4, column=1, sticky='w', padx=(0, 24), pady=(10, 0))

    # ── Validation & Save ────────────────────────────────────
    error_label = tk.Label(form, text='', font=FONTS['small'],
                            fg=COLORS['error'], bg=COLORS['card'])
    error_label.grid(row=5, column=0, columnspan=2, pady=(8, 0))

    def save():
        # Read values from each Entry
        name  = name_entry.get().strip()
        age   = age_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        gender = gender_var.get()

        # Simple validation
        if not name:
            error_label.config(text='⚠  Full Name is required.')
            name_entry.focus()
            return
        if not age.isdigit():
            error_label.config(text='⚠  Age must be a number.')
            age_entry.focus()
            return

        # Build a dictionary with patient data
        patient = {
            'name':   name,
            'age':    int(age),
            'phone':  phone,
            'email':  email,
            'gender': gender,
        }

        messagebox.showinfo("Patient Saved",
            f"Patient '{name}' added successfully!", parent=dialog)

        if on_save:
            on_save(patient)   # pass data back to main window

        dialog.destroy()       # close the dialog

    # ── Buttons ──────────────────────────────────────────────
    btn_row = tk.Frame(dialog, bg=COLORS['card'])
    btn_row.pack(fill=tk.X, padx=24, pady=16)

    cancel_btn = tk.Button(btn_row, text="Cancel", font=FONTS['btn'],
                            bg=COLORS['border'], fg=COLORS['text'],
                            relief=tk.FLAT, padx=16, pady=8, cursor='hand2',
                            command=dialog.destroy)
    cancel_btn.pack(side=tk.LEFT)

    save_canvas = make_button(btn_row, '💾  Save Patient', COLORS['accent'], save, width=148)
    save_canvas.config(bg=COLORS['card'])
    save_canvas.pack(side=tk.RIGHT)


# ─────────────────────────────────────────────────────────────
#  DIALOG 2: Add Appointment
# ─────────────────────────────────────────────────────────────

def open_appointment_dialog(parent, on_save=None):
    """
    Opens a Toplevel window with an appointment booking form.
    """

    dialog = tk.Toplevel(parent)
    dialog.title("New Appointment")
    dialog.geometry("480x420")
    dialog.config(bg=COLORS['card'])
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()

    # ── Header ───────────────────────────────────────────────
    header = tk.Frame(dialog, bg=COLORS['green'], height=54)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    tk.Label(header, text="📅  New Appointment", font=FONTS['heading'],
             fg='white', bg=COLORS['green']).pack(side=tk.LEFT, padx=20, pady=14)

    # ── Form ─────────────────────────────────────────────────
    form = tk.Frame(dialog, bg=COLORS['card'])
    form.pack(fill=tk.BOTH, expand=True)
    form.columnconfigure(1, weight=1)

    patient_entry = labeled_entry(form, "Patient Name", row=0, required=True)
    doctor_entry  = labeled_entry(form, "Doctor",       row=1, required=True)

    # Date field with today's date pre-filled
    date_entry = labeled_entry(form, "Date (YYYY-MM-DD)", row=2, required=True)
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

    time_entry = labeled_entry(form, "Time (HH:MM)", row=3)
    time_entry.insert(0, '09:00')

    # Status dropdown
    tk.Label(form, text="Status", font=FONTS['label'],
             bg=COLORS['card'], fg=COLORS['text']).grid(
                 row=4, column=0, sticky='w', padx=(24,12), pady=(10,0))

    status_var = tk.StringVar(value='Scheduled')
    status_menu = tk.OptionMenu(form, status_var, 'Scheduled', 'Completed', 'Cancelled')
    status_menu.config(font=FONTS['normal'], bg=COLORS['card'],
                       relief=tk.FLAT, highlightthickness=1,
                       highlightbackground=COLORS['border'])
    status_menu.grid(row=4, column=1, sticky='w', padx=(0,24), pady=(10,0))

    # ── Validation & Save ────────────────────────────────────
    error_label = tk.Label(form, text='', font=FONTS['small'],
                            fg=COLORS['error'], bg=COLORS['card'])
    error_label.grid(row=5, column=0, columnspan=2, pady=(8,0))

    def save():
        patient = patient_entry.get().strip()
        doctor  = doctor_entry.get().strip()
        date    = date_entry.get().strip()
        time    = time_entry.get().strip()
        status  = status_var.get()

        if not patient:
            error_label.config(text='⚠  Patient Name is required.')
            patient_entry.focus()
            return
        if not doctor:
            error_label.config(text='⚠  Doctor is required.')
            doctor_entry.focus()
            return

        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            error_label.config(text='⚠  Date must be in YYYY-MM-DD format.')
            date_entry.focus()
            return

        appointment = {
            'patient': patient,
            'doctor':  doctor,
            'date':    date,
            'time':    time,
            'status':  status,
        }

        messagebox.showinfo("Appointment Saved",
            f"Appointment for '{patient}' on {date} saved!", parent=dialog)

        if on_save:
            on_save(appointment)

        dialog.destroy()

    # ── Buttons ──────────────────────────────────────────────
    btn_row = tk.Frame(dialog, bg=COLORS['card'])
    btn_row.pack(fill=tk.X, padx=24, pady=16)

    tk.Button(btn_row, text="Cancel", font=FONTS['btn'],
              bg=COLORS['border'], fg=COLORS['text'],
              relief=tk.FLAT, padx=16, pady=8, cursor='hand2',
              command=dialog.destroy).pack(side=tk.LEFT)

    save_canvas = make_button(btn_row, '💾  Save Appointment', COLORS['green'], save, width=175)
    save_canvas.config(bg=COLORS['card'])
    save_canvas.pack(side=tk.RIGHT)


# ─────────────────────────────────────────────────────────────
#  MAIN WINDOW (to test both dialogs)
# ─────────────────────────────────────────────────────────────

root = tk.Tk()
root.title("Smart Clinic – Day 3")
root.geometry("1100x640")
root.config(bg=COLORS['bg'])

main_frame = tk.Frame(root, bg=COLORS['bg'])
main_frame.pack(fill=tk.BOTH, expand=True)

# Sidebar (same as Day 1 & 2)
sidebar = tk.Frame(main_frame, bg=COLORS['sidebar'], width=210)
sidebar.pack(side=tk.LEFT, fill=tk.Y)
sidebar.pack_propagate(False)
tk.Label(sidebar, text="Smart Clinic", font=FONTS['title'],
         fg='white', bg=COLORS['sidebar']).pack(anchor='w', padx=20, pady=(24,4))
tk.Label(sidebar, text="Management System", font=FONTS['small'],
         fg=COLORS['muted'], bg=COLORS['sidebar']).pack(anchor='w', padx=20)
tk.Frame(sidebar, bg='#2a3355', height=1).pack(fill=tk.X, pady=(16,0))
for item in ['Dashboard','Patients','Appointments','Staff','Settings']:
    tk.Label(sidebar, text=f"   {item}", font=FONTS['normal'],
             fg='#a8b8d0', bg=COLORS['sidebar'],
             anchor='w', cursor='hand2').pack(fill=tk.X, pady=2)

# Right side
right = tk.Frame(main_frame, bg=COLORS['bg'])
right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Top bar with buttons
topbar = tk.Frame(right, bg=COLORS['bg'])
topbar.pack(fill=tk.X, pady=(0, 14))

# Search (from Day 2)
search_frame = tk.Frame(topbar, bg='white',
                         highlightbackground=COLORS['border'], highlightthickness=1)
search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
tk.Label(search_frame, text='🔍', bg='white', fg=COLORS['muted']).pack(side=tk.LEFT, padx=(10,2))
tk.Entry(search_frame, font=FONTS['normal'], bg='white',
         fg=COLORS['muted'], relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True)

# Buttons — now they open real dialogs!
btn_frame = tk.Frame(topbar, bg=COLORS['bg'])
btn_frame.pack(side=tk.RIGHT, padx=(12, 0))

def on_save_patient(data):
    log.config(text=f"✅ Patient saved: {data['name']}, Age {data['age']}")

def on_save_appointment(data):
    log.config(text=f"✅ Appointment saved: {data['patient']} on {data['date']}")

# Override make_button bg for topbar context
def topbar_btn(parent, text, color, command, width=165):
    W, H, R = width, 36, 8
    canvas = tk.Canvas(parent, width=W, height=H,
                        bg=COLORS['bg'], highlightthickness=0, cursor='hand2')
    def draw(c):
        canvas.delete('all')
        canvas.create_arc(0,     0,     R*2,   R*2,   start=90,  extent=90, fill=c, outline=c)
        canvas.create_arc(W-R*2, 0,     W,     R*2,   start=0,   extent=90, fill=c, outline=c)
        canvas.create_arc(0,     H-R*2, R*2,   H,     start=180, extent=90, fill=c, outline=c)
        canvas.create_arc(W-R*2, H-R*2, W,     H,     start=270, extent=90, fill=c, outline=c)
        canvas.create_rectangle(R, 0, W-R, H, fill=c, outline=c)
        canvas.create_rectangle(0, R, W, H-R, fill=c, outline=c)
        canvas.create_text(W//2, H//2, text=text, fill='white', font=FONTS['btn'])
    def dk(h, a=25):
        return '#{:02x}{:02x}{:02x}'.format(max(0,int(h[1:3],16)-a),max(0,int(h[3:5],16)-a),max(0,int(h[5:7],16)-a))
    draw(color)
    canvas.bind('<Enter>',    lambda e: draw(dk(color)))
    canvas.bind('<Leave>',    lambda e: draw(color))
    canvas.bind('<Button-1>', lambda e: command())
    return canvas

topbar_btn(btn_frame, '＋  Add Patient',
           COLORS['accent'],
           lambda: open_patient_dialog(root, on_save_patient),
           width=148).pack(side=tk.LEFT, padx=(0,8))

topbar_btn(btn_frame, '＋  New Appointment',
           COLORS['green'],
           lambda: open_appointment_dialog(root, on_save_appointment),
           width=178).pack(side=tk.LEFT)

# Content area
card = tk.Frame(right, bg='white',
                highlightbackground=COLORS['border'], highlightthickness=1)
card.pack(fill=tk.BOTH, expand=True)

tk.Label(card, text="Click the buttons above to open dialogs",
         font=FONTS['title'], fg=COLORS['muted'], bg='white').pack(expand=True)

log = tk.Label(card, text='', font=FONTS['normal'],
               fg=COLORS['accent'], bg='white')
log.pack(pady=(0, 40))

root.mainloop()
