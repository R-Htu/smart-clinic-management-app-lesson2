import tkinter as tk
from tkinter import ttk

# ── Colors & Fonts ──────────────────────────────────────────
COLORS = {
    'bg':          '#f0f4f8',
    'sidebar':     '#1a2340',
    'sidebar_hover':   '#243054',
    'sidebar_active':  '#2e3d6e',
    'accent':      '#4f7ef8',
    'green':       '#2ec87a',
    'card':        '#ffffff',
    'text':        '#1e2d40',
    'muted':       '#8a99b0',
    'border':      '#dde3ef',
    'white':       '#ffffff',
}

FONTS = {
    'logo':     ('Segoe UI', 13, 'bold'),
    'logo_sub': ('Segoe UI', 9),
    'nav':      ('Segoe UI', 11),
    'nav_label':('Segoe UI', 8, 'bold'),
    'btn':      ('Segoe UI', 10, 'bold'),
    'search':   ('Segoe UI', 10),
}

NAV_ITEMS = [
    ('dashboard',    'Dashboard',    '⊞'),
    ('patients',     'Patients',     ''),
    ('appointments', 'Appointments', ''),
    ('---', None, None),                  # divider
    ('staff',        'Staff',        ''),
    ('settings',     'Settings',     '⚙'),
]


# ── Sidebar ─────────────────────────────────────────────────
class Sidebar(tk.Frame):
    def __init__(self, parent, on_nav):
        super().__init__(parent, bg=COLORS['sidebar'], width=210)
        self.pack_propagate(False)
        self.on_nav = on_nav
        self.active = 'dashboard'
        self.nav_buttons = {}
        self._build()

    def _build(self):
        # Logo area
        logo_frame = tk.Frame(self, bg=COLORS['sidebar'])
        logo_frame.pack(fill=tk.X, padx=20, pady=(22, 16))

        tk.Label(logo_frame, text='Smart Clinic',
                 font=FONTS['logo'], fg=COLORS['white'],
                 bg=COLORS['sidebar']).pack(anchor='w')
        tk.Label(logo_frame, text='Management System',
                 font=FONTS['logo_sub'], fg=COLORS['muted'],
                 bg=COLORS['sidebar']).pack(anchor='w')

        # Separator
        tk.Frame(self, bg='#2a3355', height=1).pack(fill=tk.X)

        # Section label: Main
        self._section_label('MAIN')

        # Nav items
        for key, label, icon in NAV_ITEMS:
            if key == '---':
                self._section_label('ADMIN', top_pad=10)
                continue
            btn = self._nav_button(key, icon, label)
            self.nav_buttons[key] = btn

        # Footer
        tk.Frame(self, bg='#2a3355', height=1).pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(self, text='v1.0  ·  Smart Clinic',
                 font=('Segoe UI', 8), fg=COLORS['muted'],
                 bg=COLORS['sidebar']).pack(side=tk.BOTTOM, pady=12)

    def _section_label(self, text, top_pad=4):
        tk.Label(self, text=text,
                 font=FONTS['nav_label'], fg=COLORS['muted'],
                 bg=COLORS['sidebar']).pack(anchor='w', padx=20,
                                            pady=(top_pad, 4))

    def _nav_button(self, key, icon, label):
        frame = tk.Frame(self, bg=COLORS['sidebar'], cursor='hand2')
        frame.pack(fill=tk.X)

        inner = tk.Frame(frame, bg=COLORS['sidebar'])
        inner.pack(fill=tk.X, padx=6)

        # Active indicator bar (left edge)
        bar = tk.Frame(inner, width=3, bg=COLORS['sidebar'])
        bar.pack(side=tk.LEFT, fill=tk.Y)

        content = tk.Frame(inner, bg=COLORS['sidebar'])
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        icon_lbl = tk.Label(content, text=icon, font=('Segoe UI', 11),
                            fg='#a8b8d0', bg=COLORS['sidebar'], width=2)
        icon_lbl.pack(side=tk.LEFT, padx=(8, 4), pady=9)

        text_lbl = tk.Label(content, text=label, font=FONTS['nav'],
                            fg='#a8b8d0', bg=COLORS['sidebar'], anchor='w')
        text_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=9)

        widgets = [frame, inner, content, icon_lbl, text_lbl, bar]

        for w in widgets:
            w.bind('<Button-1>', lambda e, k=key: self._on_click(k))
            w.bind('<Enter>', lambda e, f=frame, i=inner, c=content,
                   il=icon_lbl, tl=text_lbl, k=key: self._on_enter(f, i, c, il, tl, k))
            w.bind('<Leave>', lambda e, f=frame, i=inner, c=content,
                   il=icon_lbl, tl=text_lbl, k=key: self._on_leave(f, i, c, il, tl, k))

        return {'frame': frame, 'inner': inner, 'content': content,
                'icon': icon_lbl, 'text': text_lbl, 'bar': bar}

    def _on_click(self, key):
        self.active = key
        self._refresh_styles()
        self.on_nav(key)

    def _on_enter(self, frame, inner, content, icon_lbl, text_lbl, key):
        if key != self.active:
            for w in [frame, inner, content, icon_lbl, text_lbl]:
                w.config(bg=COLORS['sidebar_hover'])
            icon_lbl.config(fg=COLORS['white'])
            text_lbl.config(fg=COLORS['white'])

    def _on_leave(self, frame, inner, content, icon_lbl, text_lbl, key):
        if key != self.active:
            for w in [frame, inner, content, icon_lbl, text_lbl]:
                w.config(bg=COLORS['sidebar'])
            icon_lbl.config(fg='#a8b8d0')
            text_lbl.config(fg='#a8b8d0')

    def _refresh_styles(self):
        for key, widgets in self.nav_buttons.items():
            is_active = (key == self.active)
            bg = COLORS['sidebar_active'] if is_active else COLORS['sidebar']
            fg_text = COLORS['white'] if is_active else '#a8b8d0'
            bar_bg = COLORS['accent'] if is_active else COLORS['sidebar_active'] if is_active else bg

            for w_key in ['frame', 'inner', 'content', 'icon', 'text']:
                widgets[w_key].config(bg=bg)
            widgets['text'].config(fg=fg_text)
            widgets['icon'].config(fg=fg_text)
            widgets['bar'].config(bg=COLORS['accent'] if is_active else bg)

    def update_active(self, key):
        self.active = key
        self._refresh_styles()


# ── Rounded Button (via Canvas) ──────────────────────────────
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, color, command=None, width=160, height=36, radius=10):
        super().__init__(parent, width=width, height=height,
                         bg=COLORS['bg'], highlightthickness=0, cursor='hand2')
        self.color = color
        self.hover_color = self._darken(color)
        self.text = text
        self.command = command
        self.radius = radius
        self.w = width
        self.h = height
        self._draw(self.color)
        self.bind('<Button-1>', lambda e: command() if command else None)
        self.bind('<Enter>', lambda e: self._draw(self.hover_color))
        self.bind('<Leave>', lambda e: self._draw(self.color))

    def _draw(self, color):
        self.delete('all')
        r, w, h = self.radius, self.w, self.h
        self.create_arc(0, 0, r*2, r*2, start=90, extent=90, fill=color, outline=color)
        self.create_arc(w-r*2, 0, w, r*2, start=0, extent=90, fill=color, outline=color)
        self.create_arc(0, h-r*2, r*2, h, start=180, extent=90, fill=color, outline=color)
        self.create_arc(w-r*2, h-r*2, w, h, start=270, extent=90, fill=color, outline=color)
        self.create_rectangle(r, 0, w-r, h, fill=color, outline=color)
        self.create_rectangle(0, r, w, h-r, fill=color, outline=color)
        self.create_text(w//2, h//2, text=self.text,
                         fill=COLORS['white'], font=FONTS['btn'])

    def _darken(self, hex_color):
        r = max(0, int(hex_color[1:3], 16) - 20)
        g = max(0, int(hex_color[3:5], 16) - 20)
        b = max(0, int(hex_color[5:7], 16) - 20)
        return f'#{r:02x}{g:02x}{b:02x}'


# ── TopBar ───────────────────────────────────────────────────
class TopBar(tk.Frame):
    def __init__(self, parent, on_search, on_add_patient, on_add_appointment):
        super().__init__(parent, bg=COLORS['bg'])
        self.pack(fill=tk.X, pady=(0, 12))
        self._build(on_search, on_add_patient, on_add_appointment)

    def _build(self, on_search, on_add_patient, on_add_appointment):
        # Search box
        search_frame = tk.Frame(self, bg=COLORS['white'],
                                highlightbackground=COLORS['border'],
                                highlightthickness=1)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)

        tk.Label(search_frame, text='🔍', font=('Segoe UI', 10),
                 bg=COLORS['white'], fg=COLORS['muted']).pack(side=tk.LEFT, padx=(10, 4))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                     font=FONTS['search'], bg=COLORS['white'],
                                     fg=COLORS['text'], relief=tk.FLAT,
                                     insertbackground=COLORS['accent'])
        self.search_entry.insert(0, 'Search patients, appointments…')
        self.search_entry.config(fg=COLORS['muted'])
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        # Placeholder behavior
        self.search_entry.bind('<FocusIn>',  self._search_focus_in)
        self.search_entry.bind('<FocusOut>', self._search_focus_out)
        self.search_entry.bind('<Return>', lambda e: on_search())

        # Focus highlight on search frame
        self.search_entry.bind('<FocusIn>',
            lambda e, f=search_frame: (
                f.config(highlightbackground=COLORS['accent'], highlightthickness=2),
                self._search_focus_in(e)
            ), add='+')
        self.search_entry.bind('<FocusOut>',
            lambda e, f=search_frame: (
                f.config(highlightbackground=COLORS['border'], highlightthickness=1),
                self._search_focus_out(e)
            ), add='+')

        # Buttons
        btn_frame = tk.Frame(self, bg=COLORS['bg'])
        btn_frame.pack(side=tk.RIGHT, padx=(12, 0))

        RoundedButton(btn_frame, '＋  Add Patient',
                      COLORS['accent'], on_add_patient,
                      width=148, height=36).pack(side=tk.LEFT, padx=(0, 8))

        RoundedButton(btn_frame, '＋  New Appointment',
                      COLORS['green'], on_add_appointment,
                      width=178, height=36).pack(side=tk.LEFT)

    def _search_focus_in(self, e):
        if self.search_entry.get() == 'Search patients, appointments…':
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=COLORS['text'])

    def _search_focus_out(self, e):
        if not self.search_entry.get():
            self.search_entry.insert(0, 'Search patients, appointments…')
            self.search_entry.config(fg=COLORS['muted'])

    def get_search_query(self):
        val = self.search_var.get()
        return '' if val == 'Search patients, appointments…' else val

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self._search_focus_out(None)


# ── Main App ─────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Smart Clinic Management System')
        self.geometry('1200x680')
        self.config(bg=COLORS['bg'])
        self._build()

    def _build(self):
        container = tk.Frame(self, bg=COLORS['bg'])
        container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar = Sidebar(container, self.on_nav)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Right side
        right = tk.Frame(container, bg=COLORS['bg'])
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # TopBar
        self.topbar = TopBar(right,
                             on_search=self.on_search,
                             on_add_patient=self.on_add_patient,
                             on_add_appointment=self.on_add_appointment)

        # Content area
        self.content = tk.Frame(right, bg=COLORS['card'],
                                highlightbackground=COLORS['border'],
                                highlightthickness=1)
        self.content.pack(fill=tk.BOTH, expand=True)

        self._show_placeholder('Dashboard')

    def _show_placeholder(self, name):
        for w in self.content.winfo_children():
            w.destroy()
        tk.Label(self.content, text=name,
                 font=('Segoe UI', 20, 'bold'),
                 fg=COLORS['muted'], bg=COLORS['card']).pack(expand=True)

    def on_nav(self, key):
        labels = {
            'dashboard': 'Dashboard', 'patients': 'Patients',
            'appointments': 'Appointments', 'staff': 'Staff', 'settings': 'Settings'
        }
        self._show_placeholder(labels.get(key, key))

    def on_search(self):
        q = self.topbar.get_search_query()
        print(f'Search: {q}')

    def on_add_patient(self):
        print('Open Add Patient dialog')

    def on_add_appointment(self):
        print('Open New Appointment dialog')


if __name__ == '__main__':
    app = App()
    app.mainloop()