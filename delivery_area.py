'''API for managment to area'''
import sqlite3
import db


class Status400(Exception):
    '''Simulate status code 400'''
    pass


class Status404(Exception):
    '''Simulate status code 404'''
    pass


def get_id_area(coor_place):
    '''Return id of area who have coor_place'''
    if len(coor_place) != 2:
        raise Status400('Bad point')
    areas = db.get_all_areas()
    for id_area, points in areas:
        if _point_in_area(coor_place, points):
            return id_area
    raise Status404('Not found area who have this coordinate')


def get_all_areas():
    '''Return list of (id, points) of all areas'''
    return db.get_all_areas()


def add_area(points):
    '''Add new area in db

    Keyword arguments:
    points -- points of area
    '''
    try:
        if len(points) < 3 or \
                any(map(lambda point: len(point) != 2, points)):
            raise Status400('Bad points')
    except TypeError:
        raise Status400('Bad points')
    db.add_area(points)


def add_areas(area_points):
    '''Add new areas in db in one time

    Keyword arguments:
    area_points -- list of points of areas
    '''
    points_in_1d = []
    for points in area_points:
        points_in_1d += points
    if any(map(lambda points: len(points) < 3, area_points)) or \
            any(map(lambda point: len(point) != 2, points_in_1d)):
        raise Status400('Bad points')
    db.add_areas(area_points)


def get_area_points(id_area):
    '''Return area(id, points) by id'''
    try:
        return db.get_area(id_area)
    except sqlite3.Error as error:
        raise Status404 from error


def assign_courier_to_area(courier_description, id_area):
    '''Assign new courier to area

    Keyword arguments:
    courier_description -- info about courier
    id_area -- area will be assigned to courier
    '''
    try:
        db.add_courier(id_area, courier_description)
    except sqlite3.Error as error:
        raise Status404 from error


def assign_courier_for_delivery(coord_delivery):
    '''Assign courier to delivery

    Keyword arguments:
    coord_delivery -- coordinates of place delivery
    '''
    if len(coord_delivery) != 2:
        raise Status400('Bad point')

    try:
        id_area = get_id_area(coord_delivery)
    except Status400:
        raise Status400('No delivery to this place')

    try:
        courier = db.get_couriers_by_area(id_area)
    except sqlite3.Error:
        raise Status400('Now there is not courier in this area')

    courier_description = courier[0][2]
    return id_area, courier_description


def _point_in_area(point, area_points):
    '''Return true if point at area else false

    Keyword arguments:
    point -- coordinates of needed point
    area_points -- coordinates of chosen area
    '''
    if len(point) != 2:
        raise Status400('Bad point')
    x_point, y_point = point
    result = False
    x2_area, y2_area = area_points[-1]
    for x1_area, y1_area in area_points:
        if ((y1_area < y_point <= y2_area or
            y2_area < y_point <= y1_area) and
                (x1_area + (y_point - y1_area) / (y2_area - y1_area) *
                 (x2_area - x1_area) < x_point)):
            result = not result

        x2_area, y2_area = x1_area, y1_area
    return result
