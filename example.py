#!/usr/bin/env python
# -*- coding: utf-8 -*-
import WazeRouteCalculator

from_address = 'Enlace Costanera'
to_address = 'Casablanca'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address)
try:
    route.calc_route_info(debug=True)
except WazeRouteCalculator.WRCError as err:
    print err
