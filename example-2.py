import WazeRouteCalculator

from_address = (-33.43937,-70.8115) # From Santiago, Chile
to_address = (-33.05235,-71.60179)  # To Valparaiso, Chile
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, log_lvl='INFO')
route_time, route_distance = route.calc_route_info()

