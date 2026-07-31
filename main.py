from controllers.control_grand_prix import ControlGrandPrix
from views.main_window import MainWindow

main = MainWindow()
start = ControlGrandPrix(main)
start.run_race()