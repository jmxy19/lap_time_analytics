import threading
import time
import random


class ControlGrandPrix:

    # Tyre wear per lap (%) for each compound
    TYRE_WEAR_RATES = {
        "soft":         8,
        "medium":       5,
        "hard":         3,
        "intermediate": 3,
        "full wet":     2,
    }

    def __init__(self, main_window):
        self.main_window = main_window
        self.circuit     = None
        self.car         = None
        self._running    = False

        # Inject callbacks into the view so it can call back to the controller
        # The view knows NOTHING about what these functions do internally
        self.main_window.on_start_callback = self.start_simulation
        self.main_window.on_stop_callback  = self.stop_simulation


    #  Public interface called by main.py
    def run_race(self):

        pass

    #  Circuit loader — controller decides which model to instantiate

    def _load_circuit(self, name: str):

        if name == "monza":
            from models.monza import Monza
            return Monza()

        # elif name == "silverstone":
        #     from models.silverstone import Silverstone
        #     return Silverstone()

        # elif name == "spa":
        #     from models.spa import Spa
        #     return Spa()

        # Circuit not implemented yet
        return None

    #  Callback: user pressed START

    def start_simulation(self):

        # 1 — Ask the view for the current input values
        circuit_name = self.main_window.get_circuit_choice()
        self.car     = self.main_window.get_formula_car_info()
        laps         = self.main_window.get_laps()
        sprint       = self.main_window.is_sprint()

        # 2 — Load the circuit model
        self.circuit = self._load_circuit(circuit_name)

        # 3 — Validate: circuit must exist before we can simulate
        if self.circuit is None:
            self.main_window.log(
                f"Circuit '{circuit_name}' is not implemented yet.", "err"
            )
            return

        # 4 — Tell the view to switch to "running" state, then start the thread
        self._running = True
        self.main_window.simulation_started()
        self.main_window.set_status(f"Simulating {circuit_name.title()} — session 1")
        self.main_window.log(
            f"Starting simulation — Circuit: {circuit_name.title()}  |  "
            f"HP: {self.car.horsePower}  |  Torque: {self.car.maxTorque} Nm  |  "
            f"Tyres: {self.car.tiresType.title()}", "info"
        )

        threading.Thread(
            target=self._run_free_practice,
            args=(laps, sprint),
            daemon=True
        ).start()

    #  Callback: user pressed STOP

    def stop_simulation(self):
        """
        Called by the view when the user presses STOP.
        Sets the flag that the simulation thread checks each lap.
        """
        self._running = False
        self.main_window.log("Simulation stopped by user.", "warn")
        self.main_window.set_status("Stopped.")
        self.main_window.simulation_ended()

    #  Simulation logic — runs on a background thread

    def _run_free_practice(self, laps_total: int, sprint: bool):
        """
        Full free-practice simulation.
        All decisions (session changes, pit calls, wear limits) live here.
        The view only receives the final computed values to display.
        """
        tyre_key     = self.car.tiresType
        wear_rate    = self.TYRE_WEAR_RATES.get(tyre_key, 5)
        max_sessions = 2 if sprint else 3

        # Use circuit data from the model to set a realistic base lap time
        # (distance / average F1 speed gives a rough baseline in seconds)
        base_lap_s = self.circuit.distance / 65.0   # ~65 m/s average at Monza

        session    = 1
        tyre_wear  = 0
        laps_left  = laps_total
        prev_lap_s = base_lap_s

        self.main_window.log(
            f"Session {session}/{max_sessions} started — "
            f"{tyre_key.title()} compound.", "info"
        )
        self.main_window.log(
            f"Track temp: {self.circuit.typical_track_temperature_c}°C  |  "
            f"Air temp: {self.circuit.typical_air_temperature_c}°C  |  "
            f"Rain probability: {self.circuit.rain_probability_percent}%", "info"
        )

        while session <= max_sessions and self._running:

            # ── Decision: no laps left in this session → advance session ──
            if laps_left == 0:
                self.main_window.log(
                    f"Session {session} complete — all laps done.", "info"
                )
                session   += 1
                laps_left  = laps_total
                tyre_wear  = 0
                if session <= max_sessions:
                    self.main_window.log(
                        f"Session {session}/{max_sessions} started.", "info"
                    )
                    self.main_window.set_status(
                        f"Simulating {self.circuit.__class__.__name__} "
                        f"— session {session}"
                    )
                time.sleep(0.8)
                continue

            # ── Decision: tyre wear exceeded limit → box and advance session ──
            tyre_wear += wear_rate
            if tyre_wear > 100:
                self.main_window.log(
                    f"Tyre wear at {tyre_wear}% — box box box! "
                    f"Session {session} ended early.", "warn"
                )
                session   += 1
                laps_left  = laps_total
                tyre_wear  = 0
                if session <= max_sessions:
                    self.main_window.log(
                        f"Session {session}/{max_sessions} — fresh tyres fitted.", "info"
                    )
                time.sleep(0.8)
                continue

            # ── Lap time calculation ───────────────────────────────────────
            # Factors considered:
            #   random variance  : simulates driver/traffic variation
            #   tyre deg penalty : lap time grows as rubber degrades
            #   fuel effect      : lighter car = marginally faster (0.03s/kg)
            cur_lap   = laps_total - laps_left + 1
            fuel_load = self.circuit.fuel_per_lap_kg * (laps_total - cur_lap)
            fuel_delta = fuel_load * 0.03   # 0.03s per kg of fuel

            lap_s  = (base_lap_s
                      + random.uniform(-0.4, 0.6)   # lap-to-lap variance
                      + tyre_wear * 0.012            # tyre degradation penalty
                      + fuel_delta * 0.001)          # fuel weight effect

            delta_s    = lap_s - prev_lap_s
            prev_lap_s = lap_s

            # Sector splits: roughly 33 / 35 / 32 % of total lap
            s1 = lap_s * 0.334 + random.uniform(-0.15, 0.15)
            s2 = lap_s * 0.350 + random.uniform(-0.15, 0.15)
            s3 = lap_s - s1 - s2

            # Format lap time as MM:SS.mmm
            mins    = int(lap_s // 60)
            secs    = lap_s % 60
            lap_str = f"{mins:02d}:{secs:06.3f}"

            # Estimate remaining fuel
            laps_remaining = laps_left - 1
            fuel_remaining = round(self.circuit.fuel_per_lap_kg * laps_remaining, 2)

            # ERS: randomly varies between 60–100% (will be physics-based later)
            ers_pct = random.randint(60, 100)

            # ── Send all computed data to the view for display ─────────────
            # The view doesn't decide what to show — we send exactly what we want
            self.main_window.update_results({
                "lap_time_str":   lap_str,
                "delta_str":      f"{delta_s:+.3f}s",
                "delta_positive": delta_s <= 0,
                "s1": s1, "s2": s2, "s3": s3,
                "tyre_pct":  min(tyre_wear, 100),
                "lap":       f"{cur_lap}/{laps_total}",
                "session":   f"{session}/{max_sessions}",
                "fuel_kg":   f"{fuel_remaining}kg",
                "ers_pct":   f"{ers_pct}%",
            })

            # Log level: green if faster than previous lap, yellow if slower
            tag = "info" if delta_s <= 0 else "warn"
            self.main_window.log(
                f"Lap {cur_lap:>2}  {lap_str}  ({delta_s:+.3f}s)  "
                f"Tyre: {min(tyre_wear, 100)}%  Fuel: {fuel_remaining}kg",
                tag
            )

            laps_left -= 1
            time.sleep(0.9)   # paced so the UI updates are readable

        # ── Simulation finished ────────────────────────────────────────────
        if self._running:   # ended naturally, not stopped by user
            self.main_window.log("Simulation complete. Data ready for analysis.", "info")
            self.main_window.set_status("Simulation finished.")

        self._running = False
        self.main_window.simulation_ended()   # tell the view to reset the button