'''API for managment to area'''
import db


def get_id_area(coor_place):
    '''Return id of area who have coor_place'''
    areas = db.get_all_areas()
    for id_area, points in areas:
        if _point_in_area(coor_place, points):
            return id_area
    return None


def get_all_areas():
    '''Return list of (id, points) of all areas'''
    return db.get_all_areas()


def add_area(points):
    '''Add new area in db

    Keyword arguments:
    points -- points of area
    '''
    db.add_area(points)


def add_areas(area_points):
    '''Add new areas in db in one time

    Keyword arguments:
    area_points -- list of points of areas
    '''
    db.add_areas(area_points)


def get_area_points(id_area):
    '''Return area(id, points) by id'''
    return db.get_area(id_area)


def assign_courier_to_area(courier_description, id_area):
    '''Assign new courier to area

    Keyword arguments:
    courier_description -- info about courier
    id_area -- area will be assigned to courier
    '''
    db.add_courier(id_area, courier_description)


def assign_courier_for_delivery(coord_delivery):
    '''Assign courier to delivery

    Keyword arguments:
    coord_delivery -- coordinates of place delivery
    '''
    id_area = get_id_area(coord_delivery)
    courier = db.get_couriers_by_area(id_area)
    courier_description = courier[0][2]
    return id_area, courier_description


def _point_in_area(point, area_points):
    '''Return true if point at area else false

    Keyword arguments:
    point -- coordinates of needed point
    area_points -- coordinates of chosen area
    '''
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
