import csv
import json
from math import radians, sin, cos, acos


def count_ground_transportation_stops(file_name):
    streets = []
    with open(file_name, 'r', encoding='cp1251') as f:
        reader = csv.DictReader(f, delimiter=';')
        streets = [row['Street'] for row in reader]
        rows_count = len(streets)
        streets_dict = {i: streets.count(i) for i in streets}
        max_stops_street = max(streets_dict, key=streets_dict.get)

        print(f'Количество остановок: {rows_count}')
        print(f'Улица с максимальным числом остановок: {max_stops_street} - '
              f'{streets_dict[max_stops_street]} остановок')


def metro(metro_file_name, stops_file_name):
    with open(metro_file_name, encoding='cp1251') as f:
        data = json.load(f)
        stations = normalize_stations_data(data)
        stops_coordinates = get_stops_coordinates(stops_file_name)

        stations_dict = {}
        for station in stations:
            station_lon = station['coordinates'][0]
            station_lat = station['coordinates'][1]
            count = sum(get_distance(station_lon,
                                     station_lat, stop[0], stop[1]) <= 0.5
                        for stop in stops_coordinates)

            stations_dict[station['name']] = count
        max_stops_station = max(stations_dict, key=stations_dict.get)

        print('Станция метро с максимальным числом остановок в радиусе '
              f'0,5 км: {max_stops_station} - '
              f'{stations_dict[max_stops_station]} шт.')


def normalize_stations_data(data):
    grouped_stations = {}
    for station in data:
        name = station['NameOfStation']
        coordinates = station['geoData']['coordinates']
        station_group = grouped_stations.get(name, None)
        if station_group:
            grouped_stations[name].append(coordinates)
        else:
            grouped_stations[name] = [coordinates]

    stations = []
    # Calculate the center point of multiple latitude/longitude coordinates
    # Just averaging them, cause they are too close to each other
    for key, value in grouped_stations.items():
        average_coordinates = [sum(col) / len(col) for col in zip(*value)]
        stations.append({'name': key, 'coordinates': average_coordinates})

    return stations


def get_stops_coordinates(file_name):
    with open(file_name, 'r', encoding='cp1251') as f:
        reader = csv.DictReader(f, delimiter=';')
        return [[float(row['Longitude_WGS84']), float(row['Latitude_WGS84'])]
                for row in reader]


def get_distance(lon_1, lat_1, lon_2, lat_2):
    # Approximate radius of earth in km
    R = 6373.0

    start_lat = radians(lat_1)
    start_lon = radians(lon_1)
    end_lat = radians(lat_2)
    end_lon = radians(lon_2)

    distance = R * acos(sin(start_lat) * sin(end_lat)
                        + cos(start_lat) * cos(end_lat)
                        * cos(start_lon - end_lon))

    return distance


def main():
    count_ground_transportation_stops('data/data-398-2018-05-25.csv')
    metro('data/data-397-2018-03-27.json', 'data/data-398-2018-05-25.csv')


main()
