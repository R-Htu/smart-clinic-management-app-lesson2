# ============================================================
#  DAY 2 — Search Input & Buttons
#  Smart Clinic Management System
#  Topics: tk.Entry, tk.Button, tk.Canvas, events (bind),
#          hover effects, placeholder text
#  (builds on Day 1 – same window + sidebar structure)
# ============================================================

import tkinter as tk

COLORS = {
    'bg':      '#f0f4f8',
    'sidebar': '#1a2340',
    'card':    '#ffffff',
    'text':    '#1e2d40',
    'muted':   '#8a99b0',
    'accent':  '#4f7ef8',   # blue  – used for Patient button
    'green':   '#2ec87a',   # green – used for Appointment button
    'border':  '#dde3ef',
}

FONTS = {
    'title':  ('Segoe UI', 14, 'bold'),
    'normal': ('Segoe UI', 11),
    'small':  ('Segoe UI', 9),
    'btn':    ('Segoe UI', 10, 'bold'),
}

# ── Window ───────────────────────────────────────────────────
root = tk.Tk()
root.title("Smart Clinic – Day 2")
root.geometry("1100x640")
root.config(bg=COLORS['bg'])

main_frame = tk.Frame(root, bg=COLORS['bg'])
main_frame.pack(fill=tk.BOTH, expand=True)

# ── Sidebar (same as Day 1) ──────────────────────────────────
sidebar = tk.Frame(main_frame, bg=COLORS['sidebar'], width=210)
sidebar.pack(side=tk.LEFT, fill=tk.Y)
sidebar.pack_propagate(False)

tk.Label(sidebar, text="Smart Clinic", font=FONTS['title'],
         fg='white', bg=COLORS['sidebar']).pack(anchor='w', padx=20, pady=(24, 4))
tk.Label(sidebar, text="Management System", font=FONTS['small'],
         fg=COLORS['muted'], bg=COLORS['sidebar']).pack(anchor='w', padx=20)
tk.Frame(sidebar, bg='#2a3355', height=1).pack(fill=tk.X, pady=(16, 0))

for item in ['Dashboard', 'Patients', 'Appointments', 'Staff', 'Settings']:
    tk.Label(sidebar, text=f"   {item}", font=FONTS['normal'],
             fg='#a8b8d0', bg=COLORS['sidebar'],
             anchor='w', cursor='hand2').pack(fill=tk.X, pady=2)

# ── Right side ───────────────────────────────────────────────
right = tk.Frame(main_frame, bg=COLORS['bg'])
right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# ─────────────────────────────────────────────────────────────
#  TOP BAR  (this is new in Day 2)
# ─────────────────────────────────────────────────────────────
topbar = tk.Frame(right, bg=COLORS['bg'])
topbar.pack(fill=tk.X, pady=(0, 14))

# ── Part A: Search Box ───────────────────────────────────────
# We wrap the Entry in a Frame so we can add a colored border
search_frame = tk.Frame(
    topbar,
    bg=COLORS['card'],
    highlightbackground=COLORS['border'],
    highlightthickness=1,
)
search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)

# Search icon label (just a unicode magnifier)
tk.Label(search_frame, text='🔍', font=('Segoe UI', 10),
         bg=COLORS['card'], fg=COLORS['muted']).pack(side=tk.LEFT, padx=(10, 2))

# The actual Entry widget
search_entry = tk.Entry(
    search_frame,
    font=FONTS['normal'],
    bg=COLORS['card'],
    fg=COLORS['muted'],       # start grey (placeholder look)
    relief=tk.FLAT,           # no border (border is on search_frame)
    insertbackground=COLORS['accent'],  # cursor color
)
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

# Placeholder text behaviour
PLACEHOLDER = 'Search patients, appointments…'
search_entry.insert(0, PLACEHOLDER)

def on_focus_in(event):
    """Remove placeholder when user clicks the box"""
    if search_entry.get() == PLACEHOLDER:
        search_entry.delete(0, tk.END)
        search_entry.config(fg=COLORS['text'])
    # Highlight border in blue
    search_frame.config(highlightbackground=COLORS['accent'], highlightthickness=2)

def on_focus_out(event):
    """Restore placeholder if box is empty"""
    if search_entry.get() == '':
        search_entry.insert(0, PLACEHOLDER)
        search_entry.config(fg=COLORS['muted'])
    # Reset border
    search_frame.config(highlightbackground=COLORS['border'], highlightthickness=1)

def on_search(event=None):
    """Called when user presses Enter"""
    query = search_entry.get()
    if query != PLACEHOLDER:
        result_label.config(text=f'Searching for: "{query}"')

search_entry.bind('<FocusIn>',  on_focus_in)
search_entry.bind('<FocusOut>', on_focus_out)
search_entry.bind('<Return>',   on_search)   # Enter key triggers search

# ── Part B: Buttons ──────────────────────────────────────────
# We create a small helper to make colored rounded buttons
# using tk.Canvas (because tk.Button can't have rounded corners)

def make_button(parent, text, color, command):
    """Draw a rounded rectangle button on a Canvas"""
    W, H, R = 165, 36, 8     # width, height, corner radius

    canvas = tk.Canvas(parent, width=W, height=H,
                        bg=COLORS['bg'], highlightthickness=0,
                        cursor='hand2')

    def draw(c):
        """Draw the rounded rectangle with color c"""
        canvas.delete('all')
        # Four corners (arcs) + two rectangles fill the shape
        canvas.create_arc(0,   0,   R*2, R*2, start=90,  extent=90, fill=c, outline=c)
        canvas.create_arc(W-R*2, 0, W,   R*2, start=0,   extent=90, fill=c, outline=c)
        canvas.create_arc(0,   H-R*2, R*2, H,  start=180, extent=90, fill=c, outline=c)
        canvas.create_arc(W-R*2, H-R*2, W, H,  start=270, extent=90, fill=c, outline=c)
        canvas.create_rectangle(R, 0, W-R, H, fill=c, outline=c)
        canvas.create_rectangle(0, R, W, H-R, fill=c, outline=c)
        canvas.create_text(W//2, H//2, text=text,
                           fill='white', font=FONTS['btn'])

    # Darken color slightly on hover
    def darken(hex_color, amount=20):
        r = max(0, int(hex_color[1:3], 16) - amount)
        g = max(0, int(hex_color[3:5], 16) - amount)
        b = max(0, int(hex_color[5:7], 16) - amount)
        return f'#{r:02x}{g:02x}{b:02x}'

    draw(color)
    canvas.bind('<Enter>',    lambda e: draw(darken(color)))
    canvas.bind('<Leave>',    lambda e: draw(color))
    canvas.bind('<Button-1>', lambda e: command())
    return canvas

# Button callbacks
def add_patient():
    result_label.config(text='➕ Add Patient clicked!')

def new_appointment():
    result_label.config(text='📅 New Appointment clicked!')

# Button container (right side of topbar)
btn_frame = tk.Frame(topbar, bg=COLORS['bg'])
btn_frame.pack(side=tk.RIGHT, padx=(12, 0))

patient_btn = make_button(btn_frame, '＋  Add Patient',      COLORS['accent'], add_patient)
patient_btn.pack(side=tk.LEFT, padx=(0, 8))

appt_btn    = make_button(btn_frame, '＋  New Appointment',   COLORS['green'],  new_appointment)
appt_btn.pack(side=tk.LEFT)

# ── Content area ─────────────────────────────────────────────
card = tk.Frame(right, bg=COLORS['card'],
                highlightbackground=COLORS['border'], highlightthickness=1)
card.pack(fill=tk.BOTH, expand=True)

tk.Label(card, text="Content Area", font=FONTS['title'],
         fg=COLORS['muted'], bg=COLORS['card']).pack(expand=True)

# Result label — shows feedback when buttons/search are used
result_label = tk.Label(card, text="Try the search box or buttons above!",
                         font=FONTS['normal'], fg=COLORS['muted'], bg=COLORS['card'])
result_label.pack(pady=(0, 40))

root.mainloop()
