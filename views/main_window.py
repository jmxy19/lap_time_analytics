import tkinter as tk
from tkinter import ttk


# ── Palette ────────────────────────────────────────────────────────────────────
BG         = "#0a0a0a"
PANEL_BG   = "#0f0f0f"
BORDER     = "#2a2a2a"
ACCENT_RED = "#e8002d"
ACCENT_GOLD= "#c9a84c"
TEXT_PRI   = "#e0e0e0"
TEXT_SEC   = "#888888"
TEXT_GRN   = "#00e676"
TEXT_YLW   = "#ffd600"

MONO     = ("Courier New", 10)
MONO_SM  = ("Courier New", 9)
MONO_LG  = ("Courier New", 12, "bold")
MONO_TTL = ("Courier New", 11, "bold")


class MainWindow:

    # Circuits list — add new circuit names here as you implement them
    CIRCUITS = ["Monza", "Silverstone", "Spa", "Monaco", "Suzuka"]

    # ──────────────────────────────────────────────────────────────────────────
    def __init__(self):
        # Callback slot — the controller will assign its own method here
        self.on_start_callback = None

        self._sim_running = False
        self._build_window()

    #  Window construction

    def _build_window(self):
        self.root = tk.Tk()
        self.root.title("F1 LAP TIME ANALYTICS & SIMULATOR")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self._title_bar()

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", padx=8, pady=(0, 4))

        self._config_panel(body)
        self._telemetry_panel(body)

        self._log_panel()
        self._status_bar()

    def _title_bar(self):
        # Red accent stripe at the very top
        tk.Frame(self.root, bg=ACCENT_RED, height=3).pack(fill="x")

        hdr = tk.Frame(self.root, bg=PANEL_BG)
        hdr.pack(fill="x", padx=8, pady=(6, 0))

        tk.Label(hdr, text="┌" + "─"*62 + "┐",
                 font=MONO_SM, bg=PANEL_BG, fg=BORDER).pack(anchor="w")

        row = tk.Frame(hdr, bg=PANEL_BG)
        row.pack(fill="x", padx=4)

        tk.Label(row, text="⚑  F1 LAP TIME ANALYTICS & SIMULATOR",
                 font=MONO_TTL, bg=PANEL_BG, fg=TEXT_PRI).pack(side="left")

        # Live indicator dot — blinks while simulation runs
        self._live_dot = tk.Label(row, text="●", font=MONO_TTL,
                                  bg=PANEL_BG, fg=ACCENT_RED)
        self._live_dot.pack(side="right", padx=(0, 4))
        tk.Label(row, text="[ Live ]", font=MONO_SM,
                 bg=PANEL_BG, fg=TEXT_SEC).pack(side="right")

        tk.Label(hdr, text="└" + "─"*62 + "┘",
                 font=MONO_SM, bg=PANEL_BG, fg=BORDER).pack(anchor="w")

    # ── Left panel: user inputs ───────────────────────────────────────────────
    def _config_panel(self, parent):
        frame = tk.Frame(parent, bg=PANEL_BG, width=280)
        frame.pack(side="left", fill="y", padx=(0, 4), pady=4)
        frame.pack_propagate(False)

        self._section_header(frame, "⚙  CONFIGURATION (Inputs)")

        # Circuit selector
        self._field_label(frame, "Circuit:")
        self._circuit_var = tk.StringVar(value=self.CIRCUITS[0])
        self._circuit_menu = ttk.Combobox(
            frame, textvariable=self._circuit_var,
            values=self.CIRCUITS, state="readonly", font=MONO, width=22
        )
        self._style_combobox()
        self._circuit_menu.pack(fill="x", padx=10, pady=(0, 8))

        # Horsepower input
        self._field_label(frame, "Horsepower (HP):")
        self._hp_var = tk.StringVar(value="1000")
        self._make_entry(frame, self._hp_var)

        # Max torque input
        self._field_label(frame, "Max Torque (Nm):")
        self._torque_var = tk.StringVar(value="650")
        self._make_entry(frame, self._torque_var)

        # Tyre compound selector
        self._field_label(frame, "Tyre Compound:")
        self._tyre_var = tk.StringVar(value="Soft (C5)")
        ttk.Combobox(
            frame, textvariable=self._tyre_var,
            values=["Soft (C5)", "Medium (C3)", "Hard (C1)",
                    "Intermediate", "Full Wet"],
            state="readonly", font=MONO, width=22
        ).pack(fill="x", padx=10, pady=(0, 8))

        # Sprint weekend toggle
        sprint_row = tk.Frame(frame, bg=PANEL_BG)
        sprint_row.pack(fill="x", padx=10, pady=(0, 8))
        tk.Label(sprint_row, text="Sprint Weekend:",
                 font=MONO_SM, bg=PANEL_BG, fg=TEXT_SEC).pack(side="left")
        self._sprint_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            sprint_row, variable=self._sprint_var,
            bg=PANEL_BG, fg=TEXT_PRI, selectcolor=ACCENT_RED,
            activebackground=PANEL_BG, relief="flat", bd=0
        ).pack(side="left", padx=6)

        # Lap count input
        self._field_label(frame, "Laps to simulate:")
        self._laps_var = tk.StringVar(value="10")
        self._make_entry(frame, self._laps_var)

        # Start / Stop button
        tk.Frame(frame, bg=PANEL_BG, height=8).pack()
        self._start_btn = tk.Button(
            frame,
            text="▶  START SIMULATION",
            font=("Courier New", 11, "bold"),
            bg=BORDER, fg=TEXT_PRI,
            activebackground=ACCENT_RED, activeforeground="#ffffff",
            relief="flat", bd=0, cursor="hand2",
            padx=12, pady=10,
            command=self._on_start          # notifies the controller
        )
        self._start_btn.pack(fill="x", padx=10, pady=4)
        self._start_btn.bind("<Enter>",
            lambda e: self._start_btn.config(bg=ACCENT_RED, fg="#ffffff"))
        self._start_btn.bind("<Leave>",
            lambda e: self._start_btn.config(bg=BORDER, fg=TEXT_PRI))

    # ── Right panel: live telemetry ───────────────────────────────────────────
    def _telemetry_panel(self, parent):
        frame = tk.Frame(parent, bg=PANEL_BG)
        frame.pack(side="left", fill="both", expand=True, pady=4)

        self._section_header(frame, "📊  RESULTS & TELEMETRY")

        # Lap time and delta row
        lap_row = tk.Frame(frame, bg=PANEL_BG)
        lap_row.pack(fill="x", padx=12, pady=(4, 0))

        tk.Label(lap_row, text="Lap Time:", font=MONO,
                 bg=PANEL_BG, fg=TEXT_SEC).pack(side="left")
        self._lap_time_lbl = tk.Label(lap_row, text="--:--.---",
                                      font=MONO_LG, bg=PANEL_BG, fg=ACCENT_GOLD)
        self._lap_time_lbl.pack(side="left", padx=8)

        tk.Label(lap_row, text="Delta:", font=MONO,
                 bg=PANEL_BG, fg=TEXT_SEC).pack(side="left", padx=(16, 0))
        self._delta_lbl = tk.Label(lap_row, text="---",
                                   font=MONO_LG, bg=PANEL_BG, fg=TEXT_GRN)
        self._delta_lbl.pack(side="left", padx=6)
        self._delta_dot = tk.Label(lap_row, text="●",
                                   font=MONO, bg=PANEL_BG, fg=TEXT_GRN)
        self._delta_dot.pack(side="left")

        # Sector times box
        sector_box = tk.Frame(frame, bg="#161616")
        sector_box.pack(fill="x", padx=12, pady=8)
        tk.Label(sector_box, text="┌─ Sector Times " + "─"*20 + "┐",
                 font=MONO_SM, bg="#161616", fg=BORDER).pack(anchor="w", padx=4)
        self._s_labels = []
        for i in range(1, 4):
            lbl = tk.Label(sector_box, text=f"  Sector {i}:  ---.--s",
                           font=MONO, bg="#161616", fg=TEXT_SEC, anchor="w")
            lbl.pack(fill="x", padx=8, pady=1)
            self._s_labels.append(lbl)
        tk.Label(sector_box, text="└" + "─"*35 + "┘",
                 font=MONO_SM, bg="#161616", fg=BORDER).pack(anchor="w", padx=4)

        # Tyre degradation progress bar
        tk.Label(frame, text="Tyre Degradation:",
                 font=MONO, bg=PANEL_BG, fg=TEXT_SEC).pack(anchor="w", padx=12, pady=(4, 0))
        tyre_row = tk.Frame(frame, bg=PANEL_BG)
        tyre_row.pack(fill="x", padx=12, pady=(2, 6))
        self._tyre_canvas = tk.Canvas(tyre_row, bg="#161616",
                                      height=18, width=200, highlightthickness=0)
        self._tyre_canvas.pack(side="left")
        self._tyre_pct_lbl = tk.Label(tyre_row, text=" 0%",
                                      font=MONO, bg=PANEL_BG, fg=TEXT_YLW)
        self._tyre_pct_lbl.pack(side="left", padx=6)
        self._draw_tyre_bar(0)

        # Mini stats grid (Lap / Session / Fuel / ERS)
        stats_frame = tk.Frame(frame, bg=PANEL_BG)
        stats_frame.pack(fill="x", padx=12, pady=4)
        self._stat_labels = {}
        for col, (key, val) in enumerate(
                [("Lap","—"), ("Session","—"), ("Fuel","—"), ("ERS","—")]):
            cell = tk.Frame(stats_frame, bg="#161616", padx=8, pady=4)
            cell.grid(row=0, column=col, padx=3, sticky="ew")
            stats_frame.columnconfigure(col, weight=1)
            tk.Label(cell, text=key, font=MONO_SM,
                     bg="#161616", fg=TEXT_SEC).pack()
            lbl = tk.Label(cell, text=val,
                           font=("Courier New", 11, "bold"),
                           bg="#161616", fg=ACCENT_GOLD)
            lbl.pack()
            self._stat_labels[key] = lbl

    # ── Bottom: event log ─────────────────────────────────────────────────────
    def _log_panel(self):
        frame = tk.Frame(self.root, bg=PANEL_BG)
        frame.pack(fill="both", padx=8, pady=(0, 4))

        tk.Label(tk.Frame(frame, bg="#1a1a00").pack(fill="x") or frame,
                 text="▪  LOGS / TRACK EVENTS",
                 font=MONO_TTL, bg="#1a1a00",
                 fg=ACCENT_GOLD, padx=8, pady=3).pack(side="left")

        # Rewrite the log header cleanly
        hdr = tk.Frame(frame, bg="#1a1a00")
        hdr.pack(fill="x")
        tk.Label(hdr, text="▪  LOGS / TRACK EVENTS",
                 font=MONO_TTL, bg="#1a1a00",
                 fg=ACCENT_GOLD, padx=8, pady=3).pack(side="left")

        self._log_text = tk.Text(
            frame, height=5, font=MONO_SM,
            bg="#0d0d00", fg=TEXT_GRN,
            insertbackground=TEXT_GRN, relief="flat",
            bd=0, padx=6, pady=4, state="disabled", wrap="word"
        )
        self._log_text.pack(fill="both", padx=2, pady=2)
        self._log_text.tag_config("warn", foreground=TEXT_YLW)
        self._log_text.tag_config("err",  foreground=ACCENT_RED)
        self._log_text.tag_config("info", foreground=TEXT_GRN)

    def _status_bar(self):
        bar = tk.Frame(self.root, bg="#111111")
        bar.pack(fill="x", side="bottom")
        self._status_lbl = tk.Label(
            bar, text="  Ready — configure inputs and press START",
            font=MONO_SM, bg="#111111", fg=TEXT_SEC, anchor="w"
        )
        self._status_lbl.pack(side="left", pady=2)
        self._circuit_tag = tk.Label(bar, text="",
                                     font=MONO_SM, bg="#111111", fg=ACCENT_RED)
        self._circuit_tag.pack(side="right", padx=8)

    #  UI helpers

    def _section_header(self, parent, title):
        tk.Label(parent, text=f" {title} ", font=MONO_TTL,
                 bg="#1a1a1a", fg=TEXT_PRI, anchor="w",
                 padx=6, pady=4).pack(fill="x")
        tk.Frame(parent, bg=ACCENT_RED, height=1).pack(fill="x")

    def _field_label(self, parent, text):
        tk.Label(parent, text=text, font=MONO_SM,
                 bg=PANEL_BG, fg=TEXT_SEC, anchor="w"
                 ).pack(fill="x", padx=10, pady=(6, 1))

    def _make_entry(self, parent, var):
        e = tk.Entry(parent, textvariable=var, font=MONO,
                     bg="#1e1e1e", fg=TEXT_PRI, insertbackground=TEXT_PRI,
                     relief="flat", bd=0, highlightthickness=1,
                     highlightcolor=ACCENT_RED, highlightbackground=BORDER)
        e.pack(fill="x", padx=10, pady=(0, 6), ipady=5)
        return e

    def _style_combobox(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground="#1e1e1e", background="#1e1e1e",
                        foreground=TEXT_PRI, arrowcolor=ACCENT_RED,
                        bordercolor=BORDER, selectbackground="#1e1e1e",
                        selectforeground=TEXT_PRI)
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#1e1e1e")],
                  foreground=[("readonly", TEXT_PRI)])

    def _draw_tyre_bar(self, pct: int):
        """Draw the tyre degradation progress bar on the canvas."""
        c = self._tyre_canvas
        c.delete("all")
        w, h = 200, 18
        c.create_rectangle(0, 0, w, h, fill="#1e1e1e", outline="")
        fill_w = int(w * pct / 100)
        colour = TEXT_GRN if pct < 50 else (TEXT_YLW if pct < 80 else ACCENT_RED)
        if fill_w > 0:
            c.create_rectangle(0, 0, fill_w, h, fill=colour, outline="")
        c.create_rectangle(0, 0, w-1, h-1, outline=BORDER, fill="")

    def _blink_live(self):
        """Pulse the live dot while the simulation is running."""
        if not self._sim_running:
            self._live_dot.config(fg=ACCENT_RED)
            return
        current = self._live_dot.cget("fg")
        self._live_dot.config(fg=PANEL_BG if current == ACCENT_RED else ACCENT_RED)
        self.root.after(600, self._blink_live)

    #  Input readers — called by the controller to collect user data

    def get_circuit_choice(self) -> str:
        """Return the selected circuit as a lowercase string e.g. 'monza'."""
        return self._circuit_var.get().split()[0].lower()

    def get_formula_car_info(self):
        """Build and return a FormulaCar from the current UI field values."""
        from models.formula_car import FormulaCar
        hp     = float(self._hp_var.get())
        torque = float(self._torque_var.get())
        tyre   = self._tyre_var.get().split()[0].lower()   # "Soft (C5)" → "soft"
        return FormulaCar(hp, torque, tyre)

    def get_laps(self) -> int:
        """Return the number of laps the user wants to simulate."""
        return int(self._laps_var.get())

    def is_sprint(self) -> bool:
        """Return True if the sprint weekend checkbox is checked."""
        return self._sprint_var.get()

    #  Output writers — called by the controller to push data into the UI

    def log(self, msg: str, level: str = "info"):
        """
        Append a line to the event log. Thread-safe.
        level: "info" (green) | "warn" (yellow) | "err" (red)
        """
        def _do():
            self._log_text.configure(state="normal")
            self._log_text.insert("end", f"> {msg}\n", level)
            self._log_text.see("end")
            self._log_text.configure(state="disabled")
        self.root.after(0, _do)

    def update_results(self, data: dict):
        """
        Push telemetry data into the right panel.
        The controller builds this dict; the view only renders it.

        Accepted keys (all optional):
            lap_time_str    str   e.g. "01:21.054"
            delta_str       str   e.g. "+0.320s"
            delta_positive  bool  True = green, False = red
            s1, s2, s3      float sector times in seconds
            tyre_pct        int   0-100
            lap             str   e.g. "3/10"
            session         str   e.g. "1/3"
            fuel_kg         str   e.g. "12.4kg"
            ers_pct         str   e.g. "87%"
        """
        def _do():
            if "lap_time_str" in data:
                self._lap_time_lbl.config(text=data["lap_time_str"])

            if "delta_str" in data:
                colour = TEXT_GRN if data.get("delta_positive", True) else ACCENT_RED
                self._delta_lbl.config(text=data["delta_str"], fg=colour)
                self._delta_dot.config(fg=colour)

            for i, key in enumerate(("s1", "s2", "s3")):
                if key in data:
                    self._s_labels[i].config(
                        text=f"  Sector {i+1}:  {data[key]:.2f}s",
                        fg=ACCENT_GOLD
                    )

            if "tyre_pct" in data:
                pct = int(data["tyre_pct"])
                self._draw_tyre_bar(pct)
                self._tyre_pct_lbl.config(text=f" {pct}%")

            for key, ui_key in (("lap","Lap"), ("session","Session"),
                                 ("fuel_kg","Fuel"), ("ers_pct","ERS")):
                if key in data:
                    self._stat_labels[ui_key].config(text=str(data[key]))

        self.root.after(0, _do)

    def set_status(self, msg: str):
        """Update the bottom status bar. Thread-safe."""
        self.root.after(0, lambda: self._status_lbl.config(text=f"  {msg}"))

    def simulation_started(self):
        """Called by the controller when the simulation begins."""
        self._sim_running = True
        self._blink_live()
        self._circuit_tag.config(text=f"[ {self.get_circuit_choice().upper()} ]")
        self._start_btn.config(
            text="■  STOP SIMULATION",
            command=self._on_stop,
            bg="#330000", fg=ACCENT_RED
        )

    def simulation_ended(self):
        """Called by the controller when the simulation finishes or is stopped."""
        self._sim_running = False
        self.root.after(0, lambda: self._start_btn.config(
            text="▶  START SIMULATION",
            command=self._on_start,
            bg=BORDER, fg=TEXT_PRI
        ))

    #  Button handlers — translate UI events into controller calls

    def _on_start(self):
        """
        The user pressed START.
        Validate inputs locally, then hand off to the controller.
        The view does NOT decide what happens next.
        """
        # Basic input validation (view responsibility: protect against bad data)
        try:
            float(self._hp_var.get())
            float(self._torque_var.get())
            int(self._laps_var.get())
        except ValueError:
            self.log("Invalid input — check HP, Torque and Laps fields.", "err")
            return

        # Notify the controller — it will take it from here
        if self.on_start_callback:
            self.on_start_callback()

    def _on_stop(self):
        """
        The user pressed STOP.
        Notify the controller so it can cleanly halt the simulation thread.
        """
        if self.on_stop_callback:
            self.on_stop_callback()

    # ══════════════════════════════════════════════════════════════════════════
    #  Entry point
    # ══════════════════════════════════════════════════════════════════════════

    def run(self):
        """Start the Tkinter event loop. Called from main.py after MVC wiring."""
        self.root.mainloop()