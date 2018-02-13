#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from irc3.plugins.command import command
from irc3.compat import asyncio
from irc3.compat import Queue
from datetime import datetime
import irc3
import requests
import objectpath


"""
Helsinki area public transport route planning IRC bot.
"""

class HSL:
    """
    Helsinki area public transport route planning client.
    """

    def __init__(self):
        self.route_endpoint = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"
        self.map_endpoint = "https://api.digitransit.fi/geocoding/v1/search"

        # https://github.com/HSLdevcom/digitransit-ui/blob/master/app/configurations/config.hsl.js#L121
        self.AREA_POLYGON = [
            [25.5345, 60.2592],
            [25.3881, 60.1693],
            [25.3559, 60.103],
            [25.3293, 59.9371],
            [24.2831, 59.78402],
            [24.2721, 59.95501],
            [24.2899, 60.00895],
            [24.3087, 60.01947],
            [24.1994, 60.12753],
            [24.1362, 60.1114],
            [24.1305, 60.12847],
            [24.099, 60.1405],
            [24.0179, 60.1512],
            [24.0049, 60.1901],
            [24.0445, 60.1918],
            [24.0373, 60.2036],
            [24.0796, 60.2298],
            [24.1652, 60.2428],
            [24.3095, 60.2965],
            [24.3455, 60.2488],
            [24.428, 60.3002],
            [24.5015, 60.2872],
            [24.4888, 60.3306],
            [24.5625, 60.3142],
            [24.5957, 60.3242],
            [24.6264, 60.3597],
            [24.666, 60.3638],
            [24.7436, 60.3441],
            [24.9291, 60.4523],
            [24.974, 60.5253],
            [24.9355, 60.5131],
            [24.8971, 60.562],
            [25.0388, 60.5806],
            [25.1508, 60.5167],
            [25.1312, 60.4938],
            [25.0385, 60.512],
            [25.057, 60.4897],
            [25.0612, 60.4485],
            [25.1221, 60.4474],
            [25.1188, 60.4583],
            [25.149, 60.4621],
            [25.1693, 60.5062],
            [25.2242, 60.5016],
            [25.3661, 60.4118],
            [25.3652, 60.3756],
            [25.5345, 60.2592]
        ]


    def _get_coords(self, address):
        """
        Get coordinates for given address string.

        Returns a 2-tuple of floating point lon, lat coordinates.
        Returns None when no coordinates found.
        """
        if len(address) == 0:
            raise self.BadAddress("Argument 'address' is empty")

        poly = ",".join(str(x) for x in [" ".join([str(y[0]),str(y[1])]) for y in self.AREA_POLYGON])

        params = {'text': address, 'size': 1, 'boundary.polygon': poly}
        response = requests.get(self.map_endpoint, params=params)
        tree = objectpath.Tree(response.json())
        try:
            return tuple(tree.execute("$.features[0].geometry.coordinates"))
        except TypeError:
            return None

    def get_route(self, from_address, to_address, arrive = False, time = int(datetime.now().timestamp() * 1000)):

        query_text = \
        """
        {{
            plan(
                fromPlace: "{from_address}",
        """
        query_text += "from: {{lat: {from_lat}, lon: {from_lon}"
        # if not arrive:
        #     query_text += ", departureTime: {time}"
        query_text += "}},"
        query_text += "        toPlace: \"{to_address}\","
        query_text += "to: {{lat: {to_lat}, lon: {to_lon}"
        # if arrive:
        #     query_text += ", arrivalTime: {time}"
        query_text += "}},"

        query_text += \
        """
                numItineraries: 1
            ) {{
                itineraries{{
                    walkDistance,
                    duration,
                    legs {{
                        mode
                        startTime
                        endTime
                        from {{
                            name
                            stop {{
                                name
                                code
                            }}
                        }},
                        to {{
                            name
                            stop {{
                                name
                                code
                            }}
                        }},
                        distance
                        route {{
                            shortName
                        }}
                    }}
                }}
            }}
        }}
        """

        try:
            from_lon, from_lat = self._get_coords(from_address)
        except ValueError as e:
            raise self.BadAddress("No coordinates found for '%s'" % from_address)
        try:
            to_lon, to_lat = self._get_coords(to_address)
        except ValueError as e:
            raise self.BadAddress("No coordinates found for '%s'" % to_address)

        query_populated = query_text.format(from_address = from_address,
                                        to_address   = to_address,
                                        from_lat     = from_lat,
                                        from_lon     = from_lon,
                                        to_lat       = to_lat,
                                        to_lon       = to_lon)

        graphql_payload = {"query": query_populated}

        r = requests.post(self.route_endpoint, json=graphql_payload)
        return r.json()

    class BadAddress(Exception):
        pass

@irc3.plugin
class HSLbot:
    """
    Helsinki area public transport route planning IRC bot.
    """

    def __init__(self, bot):
        self.bot = bot
        self.queue = Queue()
        self.HSL = HSL()

    def _format_distance(self, meters):
        """
        Input is meters (a float).

        Output is a string representing either meters or kilometers,
        nicely rounded.
        """
        if meters < 1000:
            return str(round(meters)) + " m"
        else:
            return str(round(meters/1000, 1)) + " km"

    def _format_milliseconds(self, ms):
        """
        Print milliseconds as hours, minutes and seconds
        """
        seconds = round(ms/1000)
        hours, seconds = seconds // 3600, seconds % 3600
        minutes, seconds = seconds // 60, seconds % 60

        timestr = "{} s".format(seconds)
        if minutes > 0:
            timestr = "{} min ".format(minutes) + timestr
        if hours > 0:
            timestr = "{} h ".format(hours) + timestr

        return timestr

    def _format_seconds(self, s):
        return self._format_milliseconds(s * 1000)

    def _ms_to_time(self, ms):
        """
        Print millisecond precision UNIX timestamp as hours:minutes.
        """
        dt = datetime.fromtimestamp(ms // 1000)
        return dt.strftime("%H:%M")

    @command
    def route(self, mask, target, args):
        """Find a public transportation route. Place addresses in quotation marks if they contain spaces.

            %%route <from_address> to <to_address>
        """
        # TODO: support for departure and arrival time

        try:
            r = self.HSL.get_route(args['<from_address>'], args['<to_address>'])
        except self.HSL.BadAddress as e:
            self.bot.notice(mask.nick, str(e))
            return

        itineraries = objectpath.Tree(r).execute("$.data.plan.itineraries")
        if len(itineraries) == 0:
            self.bot.notice(mask.nick, "No routes found :(")
            return

        totaldistance = 0
        for i, itin in enumerate(itineraries):
            for leg in itin["legs"]:
                if "stop" in leg["from"] and leg["from"]["stop"] is not None:
                    from_text = "{} ({})".format(leg["from"]["stop"]["name"],
                                                 leg["from"]["stop"]["code"])
                else:
                    from_text = leg["from"]["name"]
                if "stop" in leg["to"] and leg["to"]["stop"] is not None:
                    to_text = "{} ({})".format(leg["to"]["stop"]["name"],
                                               leg["to"]["stop"]["code"])
                else:
                    to_text = leg["to"]["name"]

                if "route" in leg and leg["route"] is not None:
                    modename = " " + leg["route"]["shortName"]
                else:
                    modename = ""

                self.bot.notice(mask.nick, "Route #{num} :: {mode}{modename} at {start} from {from_} to {to} :: arrive at {end} :: distance {distance}" \
                                           .format(start = self._ms_to_time(leg["startTime"]),
                                                   end = self._ms_to_time(leg["endTime"]),
                                                   mode = leg["mode"],
                                                   modename = modename,
                                                   from_ = from_text,
                                                   to = to_text,
                                                   distance = self._format_distance(leg["distance"]),
                                                   num = i+1))

                totaldistance += leg["distance"]

            self.bot.notice(mask.nick, "Route #{num} :: Total distance {dist}, total duration {dur}" \
                            .format(num = i+1,
                                    dist = self._format_distance(totaldistance),
                                    dur = self._format_seconds(itin["duration"])))

