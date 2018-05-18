# -*- coding: utf-8 -*-
"""Waze route calculator"""

import logging
import requests


class WRCError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class WazeRouteCalculator(object):
    """Calculate actual route time and distance with Waze API"""

    WAZE_URL = "https://www.waze.com/"

    def getCoord(self,location):
        # Salida
        # Ruta 68
        if location == 'S Enlace Costanera':
             return {'lat' : -33.43937,  'lon' : -70.8115}
        elif location == 'S Casablanca':
             return {'lat' : -33.34095,  'lon' : -71.36541}
        elif location == 'S Casablanca 2':
             return {'lat' : -33.34052,  'lon' : -71.36633}
        elif location == 'S Valparaiso':
             return {'lat' : -33.05235, 'lon' : -71.60179}

        # Ruta 78
        elif location == 'S A. Vespucio':
             return {'lat' : -33.48999, 'lon' : -70.74852}
        elif location == 'S Melipilla':
             return {'lat' : -33.673829, 'lon' : -71.193956}

        # Ruta 5 Sur
        elif location == 'S Buin':
             return {'lat' : -33.70142, 'lon' : -70.72252}
        elif location == 'S Rancagua':
             return {'lat' : -34.02946, 'lon' : -70.70498}
        elif location == 'S Rancagua 2':
             return {'lat' : -34.02909, 'lon' : -70.70495}
        elif location == 'S San Fernando':
             return {'lat' : -34.57059, 'lon' : -70.97201}

        # Ruta 5 Norte
        elif location == 'S Enlace Quilicura':
             return {'lat' : -33.36821, 'lon' : -70.69922}
        elif location == 'S La Calera':
             return {'lat' : -32.78643, 'lon' : -71.17015}
        elif location == 'S La Calera 2':
             return {'lat' : -32.78708, 'lon' : -71.16934}
        elif location == 'S Los Vilos':
             return {'lat' : -33.36821, 'lon' : -70.69922}
        # Retorno
        # Ruta 68
        elif location == 'R Enlace Costanera':
             return {'lat' : -70.81089,  'lon' : -33.43964}
        elif location == 'R Casablanca':
             return {'lat' : -33.34079, 'lon' : -71.36595}
        elif location == 'R Casablanca 2':
             return {'lat' : -33.34083, 'lon' : -71.36589}
        elif location == 'R Valparaiso':
             return {'lat' : -33.05236, 'lon' : -71.60216}

        # Ruta 78
        elif location == 'R A. Vespucio':
             return {'lat' : -33.48967, 'lon' : -70.74793}
        elif location == 'R Melipilla':
             return {'lat' : -33.67308, 'lon' : -71.20159}

        # Ruta 5 Sur
        elif location == 'R Buin':
             return {'lat' : -33.70109, 'lon' : -70.72218}
        elif location == 'R Rancagua':
             return {'lat' : -34.02954, 'lon' : -70.70485}
        elif location == 'R Rancagua 2':
             return {'lat' : -34.02905, 'lon' : -70.70472}
        elif location == 'R San Fernando':
             return {'lat' : -34.57023, 'lon' : -70.97171}

        # Ruta 5 Norte
        elif location == 'R Enlace Quilicura':
             return {'lat' : -33.36737, 'lon' : -70.6999}
        elif location == 'R La Calera':
             return {'lat' : -32.77123, 'lon' :-71.18893}
        elif location == 'R La Calera 2':
             return {'lat' : -32.7873, 'lon' : -71.16949}
        elif location == 'R Los Vilos':
             return {'lat' : -31.91833, 'lon' : -71.48913}
        else:
             return None

    def __init__(self, start_address, end_address, region='EU', log_lvl=logging.INFO):
        self.log = logging.getLogger(__name__)
        if log_lvl is None:
            log_lvl = logging.WARNING
        self.log.setLevel(log_lvl)
        if not len(self.log.handlers):
            self.log.addHandler(logging.StreamHandler())
        self.log.info("From: %s - to: %s", start_address, end_address)

        region = region.upper()
        if region == 'NA':  # North America
            region = 'US'
        self.region = region

        start = self.getCoord(start_address)
        end = self.getCoord(end_address)
        if start != None:
             self.start_coords = {}
             self.start_coords['lat'] = start['lat']
             self.start_coords['lon'] = start['lon']
             self.start_coords['bounds'] = {}
        else:
             self.start_coords = self.address_to_coords(start_address)
             self.log.debug('Start coords: (%s, %s)', self.start_coords["lon"], self.start_coords["lat"])
        if end != None:
             self.end_coords = {}
             self.end_coords['lat'] = end['lat']
             self.end_coords['lon'] = end['lon']
             self.end_coords['bounds'] = {}
        else:
             self.end_coords = self.address_to_coords(end_address)
             self.log.debug('End coords: (%s, %s)', self.end_coords["lon"], self.end_coords["lat"])

    def address_to_coords(self, address):
        """Convert address to coordinates"""

        EU_BASE_COORDS = {"lon": 19.040, "lat": 47.498}
        US_BASE_COORDS = {"lon": -74.006, "lat": 40.713}
        IL_BASE_COORDS = {"lon": 35.214, "lat": 31.768}
        BASE_COORDS = dict(US=US_BASE_COORDS, EU=EU_BASE_COORDS, IL=IL_BASE_COORDS)[self.region]
        # the origin of the request can make a difference in the result

        get_cords = "SearchServer/mozi?"
        url_options = {
            "q": address,
            "lang": "eng",
            "origin": "livemap",
            "lon": BASE_COORDS["lon"],
            "lat": BASE_COORDS["lat"]
        }
        response = requests.get(self.WAZE_URL + get_cords, params=url_options)
        response_json = response.json()[0]
        lon = response_json['location']['lon']
        lat = response_json['location']['lat']
        bounds = response_json['bounds']  # sometimes the coords don't match up
        if bounds is not None:
            bounds['top'], bounds['bottom'] = max(bounds['top'], bounds['bottom']), min(bounds['top'], bounds['bottom'])
            bounds['left'], bounds['right'] = min(bounds['left'], bounds['right']), max(bounds['left'], bounds['right'])
        else:
            bounds = {}

        return {"lon": lon, "lat": lat, "bounds": bounds}

    def get_route(self, npaths=1, time_delta=0):
        """Get route data from waze"""

        routing_req_eu = "row-RoutingManager/routingRequest?"
        routing_req_us_canada = "RoutingManager/routingRequest"
        routing_req_israel = "il-RoutingManager/routingRequest"
        routing_req = dict(US=routing_req_us_canada, EU=routing_req_eu, IL=routing_req_israel)[self.region]

        url_options = {
            "from": "x:%s y:%s" % (self.start_coords["lon"], self.start_coords["lat"]),
            "to": "x:%s y:%s" % (self.end_coords["lon"], self.end_coords["lat"]),
            "at": time_delta,
            "returnJSON": "true",
            "returnGeometries": "true",
            "returnInstructions": "true",
            "timeout": 60000,
            "nPaths": npaths,
            "options": "AVOID_TRAILS:t",
        }

        headers = {'referer': 'https://www.waze.com'}

        response = requests.get(self.WAZE_URL + routing_req, params=url_options, headers=headers)
        response_json = response.json()
        if response_json.get("error"):
            raise WRCError(response_json.get("error"))
        if response_json.get("alternatives"):
            return [alt['response'] for alt in response_json['alternatives']]
        if npaths > 1:
            return [response_json['response']]
        return response_json['response']

    def _add_up_route(self, results, real_time=True, stop_at_bounds=False):
        """Calculate route time and distance."""

        start_bounds = self.start_coords['bounds']
        end_bounds = self.end_coords['bounds']

        def between(target, min, max):
            return target > min and target < max

        time = 0
        distance = 0
        for segment in results:
            if stop_at_bounds and segment.get('path'):
                x = segment['path']['x']
                y = segment['path']['y']
                if (
                    between(x, start_bounds.get('left', 0), start_bounds.get('right', 0)) or
                    between(x, end_bounds.get('left', 0), end_bounds.get('right', 0))
                ) and (
                    between(y, start_bounds.get('bottom', 0), start_bounds.get('top', 0)) or
                    between(y, end_bounds.get('bottom', 0), end_bounds.get('top', 0))
                ):
                    continue
            time += segment['crossTime' if real_time else 'crossTimeWithoutRealTime']
            distance += segment['length']
        route_time = time / 60.0
        route_distance = distance / 1000.0
        return route_time, route_distance

    def calc_route_info(self, real_time=True, stop_at_bounds=False, time_delta=0,debug=False):
        """Calculate best route info."""

        route = self.get_route(1, time_delta)
        results = route['results']
        route_time, route_distance = self._add_up_route(results, real_time=real_time, stop_at_bounds=stop_at_bounds)
        if debug:
            self.log.info('Time %.2f minutes, distance %.2f km.', route_time, route_distance)
        return route_time, route_distance

    def calc_all_routes_info(self, npaths=3, real_time=True, stop_at_bounds=False, time_delta=0):
        """Calculate all route infos."""

        routes = self.get_route(npaths, time_delta)
        results = {route['routeName']: self._add_up_route(route['results'], real_time=real_time, stop_at_bounds=stop_at_bounds) for route in routes}
        route_time = [route[0] for route in results.values()]
        route_distance = [route[1] for route in results.values()]
        self.log.info('Time %.2f - %.2f minutes, distance %.2f - %.2f km.', min(route_time), max(route_time), min(route_distance), max(route_distance))
        return results
