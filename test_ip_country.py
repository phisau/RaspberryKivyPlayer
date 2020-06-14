from geoip import geolite2
match = geolite2.lookup(['9.9.9.9'])
print(match.country.decode('UTF-8'))
