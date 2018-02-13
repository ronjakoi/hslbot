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

    def _get_coords(self, address):
        """
        Get coordinates for given address string.

        Returns a 2-tuple of floating point lon, lat coordinates.
        Returns None when no coordinates found.
        """
        if len(address) == 0:
            raise self.BadAddress("Argument 'address' is empty")
        params = {'text': address, 'size': 1}
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
            self.bot.notice(mask.nick, e)
            return

        itineraries = objectpath.Tree(r).execute("$.data.plan.itineraries")
        if len(itineraries) == 0:
            self.bot.notice(mask.nick, "No routes found :(")
            return
        
        for i, itin in enumerate(itineraries):
            for leg in itin["legs"]:
                if "stop" in leg["from"] and leg["from"]["stop"] is not None:
                    from_text = leg["from"]["stop"]["name"]
                else:
                    from_text = leg["from"]["name"]
                if "stop" in leg["to"] and leg["to"]["stop"] is not None:
                    to_text = leg["to"]["stop"]["name"]
                else:
                    to_text = leg["to"]["name"]
                self.bot.notice(mask.nick, "Route #{num} :: {mode} at {start} from {from_} to {to} :: arrive at {end} :: distance {distance}" \
                                           .format(start = self._ms_to_time(leg["startTime"]),
                                                   end = self._ms_to_time(leg["endTime"]),
                                                   mode = leg["mode"],
                                                   from_ = from_text,
                                                   to = to_text,
                                                   distance = self._format_distance(leg["distance"]),
                                                   num = i+1))
            self.bot.notice(mask.nick, "Route #{num} :: Total distance {dist}, total duration {dur}" \
                                           .format(num = i+1,
                                                   dist = self._format_distance(itin["walkDistance"]),
                                                   dur = self._format_seconds(itin["duration"])))