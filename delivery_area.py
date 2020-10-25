import db

def get_id_area(coor_place):
    areas = db.get_all_areas()
    for id_area, points in areas:
        if _point_in_area(coor_place, points):
            return id_area

def get_all_areas():
    return db.get_all_areas()

def add_area(points):
    db.add_area(points)
    
def add_areas(area_points):
    db.add_areas(area_points)

def get_area_points(id_area):
    return db.get_area(id_area)

def assign_courier_to_area(courier_description, id_area):
    db.add_courier(id_area, courier_description)
    
def assign_courier_for_delivery(coord_delivery):
    id_area = get_id_area(coord_delivery)
    courier = db.get_couriers_by_area(id_area)
    courier_description = courier[0][2]
    return id_area, courier_description

def _point_in_area(point, area_points):
    X, Y = point
    result = False
    j = len(area_points) - 1
    for i in range(len(area_points)):
        x1, y1 = area_points[i]
        x2, y2 = area_points[j]
        j = i
        if ( (y1 < Y and y2 >= Y or y2 < Y and y1 >= Y) and
                (x1 + (Y - y1) / (y2 - y1) * (x2 - x1) < X) ):
            result = not result
    return result