#!/usr/bin/env python
# -*- coding: utf-8 -*-
import WazeRouteCalculator

from_address = (-33.43937,-70.8115) # From Santiago
to_address = (-33.05235,-71.60179)  # To Valparaiso 
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address)
try:
    route.calc_route_info()
except WazeRouteCalculator.WRCError as err:
    print(err)
