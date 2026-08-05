import tkinter as tk
from tkinter import ttk
import threading
import time
import random


# ── Palette ────────────────────────────────────────────────────────────────────
BG          = "#0a0a0a"
PANEL_BG    = "#0f0f0f"
BORDER      = "#2a2a2a"
ACCENT_RED  = "#e8002d"       # F1 red
ACCENT_GOLD = "#c9a84c"       # sector gold
TEXT_PRI    = "#e0e0e0"
TEXT_SEC    = "#888888"
TEXT_GRN    = "#00e676"       # positive delta
TEXT_YLW    = "#ffd600"       # warning / tyre
MONO        = ("Courier New", 10)
MONO_SM     = ("Courier New", 9)
MONO_LG     = ("Courier New", 12, "bold")
MONO_TTL    = ("Courier New", 11, "bold")


class MainWindow:
    
    # ── available circuits  ─────────────────────────
    CIRCUITS = ["Monza"]

    # ── tyre wear per lap (%) by compound ───────────────────────────────────
    TYRE_WEAR_RATES = {
        "soft":         8,
        "medium":       5,
        "hard":         3,
        "intermediate": 3,
        "full wet":     2,
    }

    # ────────────────────────────────────────────────────────────────────────
    def __init__(self):
        self.formulaCar = None
        self.circuit    = None
        self.sprint     = False
        self._sim_running = False

        self._build_window()

    # ══════════════════════════════════════════════════════════════════════════
    #  Window construction
    # ══════════════════════════════════════════════════════════════════════════
    def _build_window(self):
        self.root = tk.Tk()
        self.root.title("F1 LAP TIME ANALYTICS & SIMULATOR")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # ── title bar ───────────────────────────────────────────────────────
        self._title_bar()

        # ── main body: left config | right telemetry ─────────────────────
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", padx=8, pady=(0, 4))

        self._config_panel(body)
        self._telemetry_panel(body)

        # ── log panel ───────────────────────────────────────────────────────
        self._log_panel()

        # ── status bar ──────────────────────────────────────────────────────
        self._status_bar()

    # ── Title bar ────────────────────────────────────────────────────────────
    def _title_bar(self):
        bar = tk.Frame(self.root, bg=ACCENT_RED, height=3)
        bar.pack(fill="x")

        hdr = tk.Frame(self.root, bg=PANEL_BG, bd=0)
        hdr.pack(fill="x", padx=8, pady=(6, 0))

        # dashed border top
        tk.Label(hdr, text="┌" + "─"*62 + "┐",
                 font=MONO_SM, bg=PANEL_BG, fg=BORDER).pack(anchor="w")

        row = tk.Frame(hdr, bg=PANEL_BG)
        row.pack(fill="x", padx=4)

        tk.Label(row, text="⚑  F1 LAP TIME ANALYTICS & SIMULATOR",
                 font=MONO_TTL, bg=PANEL_BG, fg=TEXT_PRI).pack(side="left")

        self._live_dot = tk.Label(row, text="●", font=MONO_TTL,
                                  bg=PANEL_BG, fg=ACCENT_RED)
        self._live_dot.pack(side="right", padx=(0, 4))
        tk.Label(row, text="[ ", font=MONO_SM,
                 bg=PANEL_BG, fg=TEXT_SEC).pack(side="right")
        tk.Label(row, text=" Live ]", font=MONO_SM,
                 bg=PANEL_BG, fg=TEXT_SEC).pack(side="right")

        tk.Label(hdr, text="└" + "─"*62 + "┘",
                 font=MONO_SM, bg=PANEL_BG, fg=BORDER).pack(anchor="w")

    # ── Left: Configuration panel ─────────────────────────────────────────
    def _config_panel(self, parent):
        frame = tk.Frame(parent, bg=PANEL_BG, width=280)
        frame.pack(side="left", fill="y", padx=(0, 4), pady=4)
        frame.pack_propagate(False)

        self._section_header(frame, "⚙  CONFIGURATION (Inputs)")

        # Circuit
        self._field_label(frame, "Circuit:")
        self._circuit_var = tk.StringVar(value=self.CIRCUITS[0])
        self._circuit_menu = ttk.Combobox(
            frame, textvariable=self._circuit_var,
            values=self.CIRCUITS, state="readonly",
            font=MONO, width=22
        )
        self._style_combobox()
        self._circuit_menu.pack(fill="x", padx=10, pady=(0, 8))

        # HP
        self._field_label(frame, "Horsepower (HP):")
        self._hp_var = tk.StringVar(value="1000")
        self._hp_entry = self._make_entry(frame, self._hp_var)

        # Torque
        self._field_label(frame, "Max Torque (Nm):")
        self._torque_var = tk.StringVar(value="650")
        self._torque_entry = self._make_entry(frame, self._torque_var)

        # Tyre compound
        self._field_label(frame, "Tyre Compound:")
        self._tyre_var = tk.StringVar(value="Soft (C5)")
        compounds = ["Soft (C5)", "Medium (C3)", "Hard (C1)",
                     "Intermediate", "Full Wet"]
        self._tyre_menu = ttk.Combobox(
            frame, textvariable=self._tyre_var,
            values=compounds, state="readonly",
            font=MONO, width=22
        )
        self._tyre_menu.pack(fill="x", padx=10, pady=(0, 8))

        # Sprint toggle
        sprint_row = tk.Frame(frame, bg=PANEL_BG)
        sprint_row.pack(fill="x", padx=10, pady=(0, 8))
        tk.Label(sprint_row, text="Sprint Weekend:",
                 font=MONO_SM, bg=PANEL_BG, fg=TEXT_SEC).pack(side="left")
        self._sprint_var = tk.BooleanVar(value=False)
        sprint_chk = tk.Checkbutton(
            sprint_row, variable=self._sprint_var,
            bg=PANEL_BG, fg=TEXT_PRI,
            selectcolor=ACCENT_RED, activebackground=PANEL_BG,
            relief="flat", bd=0
        )
        sprint_chk.pack(side="left", padx=6)

        # Lap count
        self._field_label(frame, "Laps to simulate:")
        self._laps_var = tk.StringVar(value="10")
        self._make_entry(frame, self._laps_var)

        # Start button
        tk.Frame(frame, bg=PANEL_BG, height=8).pack()
        self._start_btn = tk.Button(
            frame,
            text="▶  START SIMULATION",
            font=("Courier New", 11, "bold"),
            bg=BORDER, fg=TEXT_PRI,
            activebackground=ACCENT_RED, activeforeground="#ffffff",
            relief="flat", bd=0, cursor="hand2",
            padx=12, pady=10,
            command=self._on_start
        )
        self._start_btn.pack(fill="x", padx=10, pady=4)
        self._start_btn.bind("<Enter>",
            lambda e: self._start_btn.config(bg=ACCENT_RED, fg="#ffffff"))
        self._start_btn.bind("<Leave>",
            lambda e: self._start_btn.config(bg=BORDER, fg=TEXT_PRI))

    # ── Right: Telemetry / results panel ─────────────────────────────────
    def _telemetry_panel(self, parent):
        frame = tk.Frame(parent, bg=PANEL_BG)
        frame.pack(side="left", fill="both", expand=True, pady=4)

        self._section_header(frame, "📊  RESULTS & TELEMETRY")

        # Lap time + delta row
        lap_row = tk.Frame(frame, bg=PANEL_BG)
        lap_row.pack(fill="x", padx=12, pady=(4, 0))

        tk.Label(lap_row, text="Lap Time:", font=MONO, bg=PANEL_BG,
                 fg=TEXT_SEC).pack(side="left")
        self._lap_time_lbl = tk.Label(lap_row, text="--:--.---",
                                      font=MONO_LG, bg=PANEL_BG, fg=ACCENT_GOLD)
        self._lap_time_lbl.pack(side="left", padx=8)

        tk.Label(lap_row, text="Delta:", font=MONO, bg=PANEL_BG,
                 fg=TEXT_SEC).pack(side="left", padx=(16, 0))
        self._delta_lbl = tk.Label(lap_row, text="---", font=MONO_LG,
                                   bg=PANEL_BG, fg=TEXT_GRN)
        self._delta_lbl.pack(side="left", padx=6)
        self._delta_dot = tk.Label(lap_row, text="●", font=MONO,
                                   bg=PANEL_BG, fg=TEXT_GRN)
        self._delta_dot.pack(side="left")

        # Sector box
        sector_box = tk.Frame(frame, bg="#161616", bd=0)
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

        # Tyre degradation bar
        tk.Label(frame, text="Tyre Degradation:",
                 font=MONO, bg=PANEL_BG, fg=TEXT_SEC).pack(anchor="w", padx=12, pady=(4, 0))

        tyre_row = tk.Frame(frame, bg=PANEL_BG)
        tyre_row.pack(fill="x", padx=12, pady=(2, 6))

        self._tyre_canvas = tk.Canvas(tyre_row, bg="#161616", height=18,
                                      width=200, highlightthickness=0)
        self._tyre_canvas.pack(side="left")
        self._tyre_pct_lbl = tk.Label(tyre_row, text=" 0%",
                                      font=MONO, bg=PANEL_BG, fg=TEXT_YLW)
        self._tyre_pct_lbl.pack(side="left", padx=6)

        self._draw_tyre_bar(0)

        # Mini stats grid
        stats_frame = tk.Frame(frame, bg=PANEL_BG)
        stats_frame.pack(fill="x", padx=12, pady=4)

        self._stat_labels = {}
        stats = [
            ("Lap",   "—"), ("Session", "—"),
            ("Fuel",  "—"), ("ERS",     "—"),
        ]
        for col, (key, val) in enumerate(stats):
            cell = tk.Frame(stats_frame, bg="#161616", padx=8, pady=4)
            cell.grid(row=0, column=col, padx=3, sticky="ew")
            stats_frame.columnconfigure(col, weight=1)
            tk.Label(cell, text=key, font=MONO_SM,
                     bg="#161616", fg=TEXT_SEC).pack()
            lbl = tk.Label(cell, text=val, font=("Courier New", 11, "bold"),
                           bg="#161616", fg=ACCENT_GOLD)
            lbl.pack()
            self._stat_labels[key] = lbl

    # ── Bottom: Log panel ─────────────────────────────────────────────────
    def _log_panel(self):
        frame = tk.Frame(self.root, bg=PANEL_BG)
        frame.pack(fill="both", padx=8, pady=(0, 4))

        hdr_row = tk.Frame(frame, bg="#1a1a00")
        hdr_row.pack(fill="x")
        tk.Label(hdr_row, text="▪  LOGS / TRACK EVENTS",
                 font=MONO_TTL, bg="#1a1a00",
                 fg=ACCENT_GOLD, padx=8, pady=3).pack(side="left")

        self._log_text = tk.Text(
            frame, height=5, font=MONO_SM,
            bg="#0d0d00", fg=TEXT_GRN,
            insertbackground=TEXT_GRN, relief="flat",
            bd=0, padx=6, pady=4, state="disabled",
            wrap="word"
        )
        self._log_text.pack(fill="both", padx=2, pady=2)
        self._log_text.tag_config("warn", foreground=TEXT_YLW)
        self._log_text.tag_config("err",  foreground=ACCENT_RED)
        self._log_text.tag_config("info", foreground=TEXT_GRN)

    # ── Status bar ────────────────────────────────────────────────────────
    def _status_bar(self):
        bar = tk.Frame(self.root, bg="#111111")
        bar.pack(fill="x", side="bottom")
        self._status_lbl = tk.Label(
            bar, text="  Ready — configure inputs and press START",
            font=MONO_SM, bg="#111111", fg=TEXT_SEC, anchor="w"
        )
        self._status_lbl.pack(side="left", pady=2)

        # Circuit info tag (right side)
        self._circuit_tag = tk.Label(
            bar, text="", font=MONO_SM, bg="#111111", fg=ACCENT_RED
        )
        self._circuit_tag.pack(side="right", padx=8)

    # ══════════════════════════════════════════════════════════════════════════
    #  Helpers
    # ══════════════════════════════════════════════════════════════════════════
    def _section_header(self, parent, title):
        tk.Label(parent, text=f" {title} ",
                 font=MONO_TTL, bg="#1a1a1a",
                 fg=TEXT_PRI, anchor="w", padx=6, pady=4
                 ).pack(fill="x")
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
                        fieldbackground="#1e1e1e",
                        background="#1e1e1e",
                        foreground=TEXT_PRI,
                        arrowcolor=ACCENT_RED,
                        bordercolor=BORDER,
                        selectbackground="#1e1e1e",
                        selectforeground=TEXT_PRI)
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#1e1e1e")],
                  foreground=[("readonly", TEXT_PRI)])

    def _draw_tyre_bar(self, pct: int):
        c = self._tyre_canvas
        c.delete("all")
        w, h = 200, 18
        # background
        c.create_rectangle(0, 0, w, h, fill="#1e1e1e", outline="")
        # fill
        fill_w = int(w * pct / 100)
        colour = TEXT_GRN if pct < 50 else (TEXT_YLW if pct < 80 else ACCENT_RED)
        if fill_w > 0:
            c.create_rectangle(0, 0, fill_w, h, fill=colour, outline="")
        # border
        c.create_rectangle(0, 0, w-1, h-1, outline=BORDER, fill="")

    def _blink_live(self):
        """Pulse the live dot while simulation is running."""
        if not self._sim_running:
            self._live_dot.config(fg=ACCENT_RED)
            return
        current = self._live_dot.cget("fg")
        next_c  = PANEL_BG if current == ACCENT_RED else ACCENT_RED
        self._live_dot.config(fg=next_c)
        self.root.after(600, self._blink_live)

    # ══════════════════════════════════════════════════════════════════════════
    #  Public API — controller calls these
    # ══════════════════════════════════════════════════════════════════════════
    def log(self, msg: str, level: str = "info"):
        """Append a timestamped line to the event log. Thread-safe."""
        def _do():
            self._log_text.configure(state="normal")
            prefix = f"> {msg}\n"
            self._log_text.insert("end", prefix, level)
            self._log_text.see("end")
            self._log_text.configure(state="disabled")
        self.root.after(0, _do)

    def update_results(self, data: dict):
        """
        Push telemetry into the right panel.
        Expected keys (all optional):
            lap_time_str, delta_str, delta_positive,
            s1, s2, s3, tyre_pct, lap, session, fuel_kg, ers_pct
        """
        def _do():
            if "lap_time_str" in data:
                self._lap_time_lbl.config(text=data["lap_time_str"])
            if "delta_str" in data:
                pos = data.get("delta_positive", True)
                colour = TEXT_GRN if pos else ACCENT_RED
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
            for key, ui_key in (("lap","Lap"),("session","Session"),
                                 ("fuel_kg","Fuel"),("ers_pct","ERS")):
                if key in data and ui_key in self._stat_labels:
                    self._stat_labels[ui_key].config(text=str(data[key]))
        self.root.after(0, _do)

    def set_status(self, msg: str):
        self.root.after(0, lambda: self._status_lbl.config(text=f"  {msg}"))

    def get_circuit_choice(self) -> str:
        """Return the selected circuit name (lowercase)."""
        return self._circuit_var.get().split()[0].lower()

    def get_formula_car_info(self):
        """Build and return a FormulaCar from current UI values."""
        from models.formula_car import FormulaCar
        hp     = float(self._hp_var.get())
        torque = float(self._torque_var.get())
        raw    = self._tyre_var.get()          # e.g. "Soft (C5)"
        tyre   = raw.split()[0].lower()        # → "soft"
        self.formulaCar = FormulaCar(hp, torque, tyre)
        return self.formulaCar

    def is_sprint(self) -> bool:
        return self._sprint_var.get()

    # ══════════════════════════════════════════════════════════════════════════
    #  Free Practice simulation (runs on background thread)
    # ══════════════════════════════════════════════════════════════════════════
    def freePractice(self):
        """Run the free-practice simulation, pushing updates to the UI."""
        try:
            laps_total = int(self._laps_var.get())
        except ValueError:
            self.log("Invalid lap count — defaulting to 10.", "warn")
            laps_total = 10

        car        = self.formulaCar
        tyre_key   = car.tiresType          # already lowercased
        wear_rate  = self.TYRE_WEAR_RATES.get(tyre_key, 5)
        max_sessions = 2 if self.is_sprint() else 3

        def _run():
            self._sim_running = True
            self.root.after(0, self._blink_live)
            self.root.after(0, lambda: self._start_btn.config(
                text="■  STOP SIMULATION", command=self._stop_sim,
                bg="#330000", fg=ACCENT_RED))

            session      = 1
            base_lap_s   = 81.054          # Monza reference lap in seconds
            prev_lap_s   = base_lap_s

            self.log(f"Session {session} started — {tyre_key.title()} compound.", "info")
            self.log(f"Track temperature: 42°C.  Air: 27°C.", "info")
            self.set_status(f"Session {session} / {max_sessions}  |  running…")

            tyre_wear  = 0
            laps_left  = laps_total

            while session <= max_sessions and self._sim_running:
                if laps_left == 0:
                    self.log(f"Session {session} complete — all laps done.", "info")
                    session   += 1
                    laps_left  = laps_total
                    tyre_wear  = 0
                    if session <= max_sessions:
                        self.log(f"Session {session} started.", "info")
                        self.set_status(f"Session {session} / {max_sessions}  |  running…")
                    time.sleep(0.6)
                    continue

                tyre_wear += wear_rate
                if tyre_wear > 100:
                    self.log(f"Tyre wear critical ({tyre_wear}%) — box box box!", "warn")
                    self.log(f"Session {session} ended early.  Next session…", "warn")
                    session   += 1
                    laps_left  = laps_total
                    tyre_wear  = 0
                    if session <= max_sessions:
                        self.log(f"Session {session} started — fresh tyres.", "info")
                        self.set_status(f"Session {session} / {max_sessions}  |  running…")
                    time.sleep(0.6)
                    continue

                # ── Simulate lap time ────────────────────────────────────
                noise    = random.uniform(-0.4, 0.6)
                wear_pen = tyre_wear * 0.012          # tyre deg penalty
                lap_s    = base_lap_s + noise + wear_pen
                delta_s  = lap_s - prev_lap_s
                prev_lap_s = lap_s

                # sector split: roughly 33/35/32 % of lap
                s1 = lap_s * 0.334 + random.uniform(-0.15, 0.15)
                s2 = lap_s * 0.350 + random.uniform(-0.15, 0.15)
                s3 = lap_s - s1 - s2

                mins = int(lap_s // 60)
                secs = lap_s % 60
                lap_str   = f"{mins:02d}:{secs:06.3f}"
                delta_str = f"{delta_s:+.3f}s"
                cur_lap   = laps_total - laps_left + 1
                fuel_rem  = round(car.horsePower * 0.00178 * (laps_total - cur_lap + 1) / 10, 2)

                self.update_results({
                    "lap_time_str":  lap_str,
                    "delta_str":     delta_str,
                    "delta_positive": delta_s <= 0,
                    "s1": s1, "s2": s2, "s3": s3,
                    "tyre_pct": min(tyre_wear, 100),
                    "lap":     f"{cur_lap}/{laps_total}",
                    "session": f"{session}/{max_sessions}",
                    "fuel_kg": f"{fuel_rem}kg",
                    "ers_pct": f"{random.randint(60,100)}%",
                })

                tag = "info" if delta_s <= 0 else "warn"
                self.log(
                    f"Lap {cur_lap:>2}  {lap_str}  ({delta_str})  "
                    f"Tyre: {tyre_wear}%", tag
                )
                laps_left -= 1
                time.sleep(0.9)           # pace the display

            # ── Done ────────────────────────────────────────────────────
            self._sim_running = False
            self.log("Simulation complete.  Session data saved.", "info")
            self.set_status("Simulation finished.")
            self.root.after(0, lambda: self._start_btn.config(
                text="▶  START SIMULATION", command=self._on_start,
                bg=BORDER, fg=TEXT_PRI))
            self.root.after(0, lambda: self._live_dot.config(fg=ACCENT_RED))

        threading.Thread(target=_run, daemon=True).start()

    def _stop_sim(self):
        self._sim_running = False
        self.log("Simulation stopped by user.", "warn")
        self.set_status("Stopped.")
        self._start_btn.config(text="▶  START SIMULATION",
                               command=self._on_start, bg=BORDER, fg=TEXT_PRI)

    # ══════════════════════════════════════════════════════════════════════════
    #  Button handler — bridges to controller pattern
    # ══════════════════════════════════════════════════════════════════════════
    def _on_start(self):
        """Called when the user presses START.  Mirrors controller.run_race()."""
        if self._sim_running:
            return

        # Validate inputs
        try:
            float(self._hp_var.get())
            float(self._torque_var.get())
            int(self._laps_var.get())
        except ValueError:
            self.log("Invalid input — check HP, Torque and Laps fields.", "err")
            return

        circuit_name = self.get_circuit_choice()
        self._circuit_tag.config(text=f"[ {circuit_name.upper()} ]")
        self.circuit = circuit_name
        self.sprint  = self.is_sprint()

        self.get_formula_car_info()

        self.log(f"Circuit: {circuit_name.title()}  |  "
                 f"HP: {self._hp_var.get()}  |  "
                 f"Torque: {self._torque_var.get()} Nm  |  "
                 f"Tyres: {self._tyre_var.get()}", "info")

        self.freePractice()

    # ══════════════════════════════════════════════════════════════════════════
    #  Entry point
    # ══════════════════════════════════════════════════════════════════════════
    def run(self):
        self.root.mainloop()


# ── Standalone entry point (bypasses MVC for quick testing) ──────────────────
if __name__ == "__main__":
    w = MainWindow()
    w.run()