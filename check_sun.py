import ephem
import math

ASTRONOMICAL_TWILIGHT_ANGLE = -18
NAUTICAL_TWILIGHT_ANGLE = -12
CIVIL_TWILIGHT_ANGLE = -6
CLOSE_TO_SUNRISE_SUNSET_ANGLE = -2

class CheckSun:
    def __init__(self, city):
        self.city = ephem.city(city)
        self.sun = ephem.Sun()

    def is_daylight(self):
        return self.get_sun_angle() > 0

    def is_sun_close_to_horizon(self, degrees=-2):
        return 0 > self.get_sun_angle() >= CLOSE_TO_SUNRISE_SUNSET_ANGLE

    def is_civil_twilight(self):
        return CLOSE_TO_SUNRISE_SUNSET_ANGLE > self.get_sun_angle() >= CIVIL_TWILIGHT_ANGLE

    def is_nautical_twilight(self):
        return CIVIL_TWILIGHT_ANGLE > self.get_sun_angle() >= NAUTICAL_TWILIGHT_ANGLE

    def is_astronomical_twilight(self):
        return NAUTICAL_TWILIGHT_ANGLE > self.get_sun_angle() >= ASTRONOMICAL_TWILIGHT_ANGLE

    def __compare(self, degrees=0):
        self.city.date = ephem.now()
        self.sun.compute(self.city)
        return self.sun.alt - ephem.degrees(math.radians(degrees))

    def get_sun_angle(self):
        self.city.date = ephem.now()
        self.sun.compute(self.city)
        return math.degrees(self.sun.alt)
 


        
    def get_profile(self):
        if self.is_daylight():
            return 'day'
        if self.is_sun_close_to_horizon():
            return 'twilight_bright'
        if self.is_civil_twilight():
            return 'twilight'
        if self.is_nautical_twilight():
            return 'nautical_twilight'
        if self.is_astronomical_twilight():
            return 'astronomical_twilight'
        return 'night'

