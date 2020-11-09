import ephem
import math

class CheckSun:
    def __init__(self, city):
        self.city = ephem.city(city)
        self.sun = ephem.Sun()

    def is_daylight(self):
        return self.__compare(0) >= 0

    def is_sun_close_to_horizon(self, degrees=-2):
        return self.__compare(degrees) >= 0 and not self.is_daylight()

    def is_civil_twilight(self):
        return self.__compare(0) < 0 and not self.is_nautical_twilight() and not self.is_astronomical_twilight()

    def is_nautical_twilight(self):
        return self.__compare(-6) < 0 and not self.is_astronomical_twilight()

    def is_astronomical_twilight(self):
        return self.__compare(-18) < 0

    def __compare(self, degrees=0):
        self.city.date = ephem.now()
        self.sun.compute(self.city)
        return self.sun.alt - ephem.degrees(math.radians(degrees))

        
    def get_profile(self):
        if self.is_daylight():
            return 'day'
        if self.is_sun_close_to_horizon():
            return 'twilight_bright'
        if self.is_civil_twilight():
            return 'twilight'
        return 'night'

