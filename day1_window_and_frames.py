# ============================================================
#  DAY 1 — Window, Labels & Frames
#  Smart Clinic Management System
#  Topics: tk.Tk, tk.Frame, tk.Label, colors, pack layout
# ============================================================

import tkinter as tk

# ── 1. Colors (we will reuse these every day) ────────────────
COLORS = {
    'bg':      '#f0f4f8',   # light grey  – main background
    'sidebar': '#1a2340',   # dark navy   – sidebar
    'card':    '#ffffff',   # white       – content cards
    'text':    '#1e2d40',   # dark        – normal text
    'muted':   '#8a99b0',   # grey        – small / hint text
    'accent':  '#4f7ef8',   # blue        – highlights
}

# ── 2. Fonts ─────────────────────────────────────────────────
FONTS = {
    'title':  ('Segoe UI', 14, 'bold'),
    'normal': ('Segoe UI', 11),
    'small':  ('Segoe UI', 9),
}

# ── 3. Create the main window ────────────────────────────────
root = tk.Tk()
root.title("Smart Clinic Management System")
root.geometry("1100x640")          # width x height
root.config(bg=COLORS['bg'])       # set window background color

# ── 4. Main container (holds sidebar + content side by side) ─
main_frame = tk.Frame(root, bg=COLORS['bg'])
main_frame.pack(fill=tk.BOTH, expand=True)
#   fill=BOTH  → stretch in both directions
#   expand=True → take all available space

# ── 5. Sidebar frame (left column) ──────────────────────────
sidebar = tk.Frame(main_frame, bg=COLORS['sidebar'], width=210)
sidebar.pack(side=tk.LEFT, fill=tk.Y)
sidebar.pack_propagate(False)      # keep fixed width=210

# Logo label inside sidebar
logo_label = tk.Label(
    sidebar,
    text="Smart Clinic",
    font=FONTS['title'],
    fg='white',
    bg=COLORS['sidebar'],
)
logo_label.pack(anchor='w', padx=20, pady=(24, 4))

# Sub-label under logo
sub_label = tk.Label(
    sidebar,
    text="Management System",
    font=FONTS['small'],
    fg=COLORS['muted'],
    bg=COLORS['sidebar'],
)
sub_label.pack(anchor='w', padx=20)

# Thin horizontal divider line
divider = tk.Frame(sidebar, bg='#2a3355', height=1)
divider.pack(fill=tk.X, pady=(16, 0))

# Nav items (just labels for now – Day 3 will make them clickable)
nav_items = ['Dashboard', 'Patients', 'Appointments', 'Staff', 'Settings']

for item in nav_items:
    nav_label = tk.Label(
        sidebar,
        text=f"   {item}",
        font=FONTS['normal'],
        fg='#a8b8d0',            # soft blue-grey text
        bg=COLORS['sidebar'],
        anchor='w',              # align text to left
        cursor='hand2',          # pointer cursor on hover
    )
    nav_label.pack(fill=tk.X, pady=2)

# ── 6. Content area (right side) ────────────────────────────
content_area = tk.Frame(main_frame, bg=COLORS['bg'])
content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# A white "card" frame inside the content area
card = tk.Frame(
    content_area,
    bg=COLORS['card'],
    highlightbackground='#dde3ef',
    highlightthickness=1,
)
card.pack(fill=tk.BOTH, expand=True)

# Title inside the card
card_title = tk.Label(
    card,
    text="Welcome to Smart Clinic",
    font=FONTS['title'],
    fg=COLORS['text'],
    bg=COLORS['card'],
)
card_title.pack(pady=(40, 8))

# Description text
card_desc = tk.Label(
    card,
    text="This is the main content area.\nSidebar navigation will go on the left.",
    font=FONTS['normal'],
    fg=COLORS['muted'],
    bg=COLORS['card'],
    justify='center',
)
card_desc.pack()

# ── 7. Start the event loop ──────────────────────────────────
root.mainloop()
#   This keeps the window open and listens for user actions
