class Monza:
    def __init__(self):

        self.sectors = 3
        self.distance = 5793 #metters
        self.corners = 11
        self.left_corners = 4
        self.right_corners = 7
        self.x_y_mode = 2
        self.pit_lane_length = 420 #metters
        self.pit_loss_seconds = 22
        self.average_track_width = 12.5 #metters
        self.altitude = 162 #metters
        self.elevation_change = 6 #metters
        self.surface_roughness = "low"
        self.grip_level = "high"
        self.fuel_consumption = "medium-high"
        self.break_wear = "high"
        self.tyre_wear = "low"
        self.engine_stress = "high"
        self.ers_usage = "high"
        self.aero_importance = "low"
        self.safety_car_probability = "medium"
        self.rain_probability = "medium"

        #sector lengths
        self.sector_1 = 1900 #metters
        self.sector_2 = 1800 #metters
        self.sector_3 = 2093 #metters

        #straights sata
        self.main_straight = 1120
        self.main_straight_x_y_mode = True
        self.curva_grande_straight = 700
        self.serraglio_straight = 850
        self.serraglio_straight_x_y_mode = True
        self.ascari_straight = 1050

        #corner data

        #corner 1
        self.t1_length = 80 #metters
        self.t1_direction = "right"
        self.t1_radius = 28 #metters
        self.t1_min_speed = 70
        self.t1_max_exit_speed = 90
        self.t1_banking = 0 #degree
        self.t1_heavy_breaking = 4 #from 0 to 4 (0 no heavy, 1 light, 2 medium, 3 hard, 4 extreme)
        #corner 2
        self.t1_length = 85 #metters
        self.t1_direction = "left"
        self.t1_radius = 30 #metters
        self.t1_min_speed = 75
        self.t1_max_exit_speed = 120
        self.t1_banking = 0 #degree
        self.t1_heavy_breaking = 0
        #corner 3
        self.t1_length = 520 #metters
        self.t1_direction = "right"
        self.t1_radius = 340 #metters
        self.t1_min_speed = 295
        self.t1_max_exit_speed = 310
        self.t1_banking = 2 #degree
        self.t1_heavy_breaking = 0     
        #corner 4
        self.t1_length = 70 #metters
        self.t1_direction = "left"
        self.t1_radius = 32 #metters
        self.t1_min_speed = 80
        self.t1_max_exit_speed = 100
        self.t1_banking = 0 #degree
        self.t1_heavy_breaking = 3
        #corner 5
        self.t1_length = 70 #metters
        self.t1_direction = "right"
        self.t1_radius = 35 #metters
        self.t1_min_speed = 90
        self.t1_max_exit_speed = 150
        self.t1_banking = 0 #degree
        self.t1_heavy_breaking = 0
        #corner 6
        self.t1_length = 170 #metters
        self.t1_direction = "right"
        self.t1_radius = 70 #metters
        self.t1_min_speed = 145
        self.t1_max_exit_speed = 200
        self.t1_banking = 1 #degree
        self.t1_heavy_breaking = 2
        #corner 7
        self.t1_length = 180 #metters
        self.t1_direction = "right"
        self.t1_radius = 95 #metters
        self.t1_min_speed = 175
        self.t1_max_exit_speed = 245
        self.t1_banking = 1 #degree
        self.t1_heavy_breaking = 1
        #corner 8
        self.t1_length = 90 #metters
        self.t1_direction = "left"
        self.t1_radius = 120 #metters
        self.t1_min_speed = 190
        self.t1_max_exit_speed = 210
        self.t1_banking = 0 #degree
        self.t1_heavy_breaking = 2
        #corner 9
        self.t1_length = 100 #metters
        self.t1_direction = "right"
        self.t1_radius = 65 #metters
        self.t1_min_speed = 170
        self.t1_max_exit_speed = 185
        self.t1_banking = 0 #degree
        self.t1_heavy_breaking = 0
        #corner 10
        self.t1_length = 100 #metters
        self.t1_direction = "left"
        self.t1_radius = 120 #metters
        self.t1_min_speed = 185
        self.t1_max_exit_speed = 220
        self.t1_banking = 0 #degree
        self.t1_heavy_breaking = 0
        #corner 11
        self.t1_length = 480 #metters
        self.t1_direction = "right"
        self.t1_radius_profile = [ #metters
                        45,
                        52,
                        60,
                        73,
                        88,
                        105,
                        125,
                        145,
                        165,
                        180
                    ]
        self.t1_min_speed = 70
        self.t1_max_exit_speed = 90
        self.t1_banking = 0 #degree
        self.t1_heavy_breaking = 1

        #tyre characteristics
        self.front_left_wear = 0 #from 0 to 3 (0 low, 1 medium, 2 high, 3 extreme)
        self.front_right_wear = 1
        self.rear_left_wear = 0
        self.rear_right_wear = 1

        #fuel
        self.fuel_per_lap_kg = 1.78

        #weather
        self.typical_air_temperature_c = 27
        self.typical_track_temperature_c =	42
        self.humidity_percent =	60
        self.wind_speed_kmh	= 10
        self.rain_probability_percent =	25
            