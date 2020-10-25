'''Module for work with database'''
import sqlite3
import pickle

HOST = 'database.db'


def connect_bd(fun):
    '''Decorator for work with database
    1st param is connect to db for fun'''
    def decorate(*args, **kwargs):
        with sqlite3.connect(HOST) as connect:
            return fun(*args, **kwargs, connect=connect)
    return decorate


@connect_bd
def _init_tables(connect=None):
    '''Create table if it is not exists'''
    connect.execute('''CREATE TABLE IF NOT EXISTS area (
                    id INTEGER PRIMARY KEY NOT NULL,
                    points NOT NULL
                    )''')

    connect.execute('''CREATE TABLE IF NOT EXISTS courier (
                    id INTEGER PRIMARY KEY NOT NULL,
                    area INTEGER NOT NULL,
                    description
                    )''')


@connect_bd
def add_area(points, connect=None):
    '''Add new area in db

    Keyword arguments:
    points -- points of area
    '''
    connect.execute('INSERT INTO area VALUES(NULL, ?)', [pickle.dumps(points)])
    connect.commit()


@connect_bd
def add_areas(areas, connect=None):
    '''Add new areas in db in one time

    Keyword arguments:
    areas -- list of points of areas
    '''
    dump_areas = [(pickle.dumps(points),) for points in areas]
    connect.executemany('INSERT INTO area VALUES(NULL, ?)', dump_areas)
    connect.commit()


@connect_bd
def get_all_areas(connect=None):
    '''Return list of (id, points) of all areas'''
    response = connect.execute('SELECT * FROM area').fetchall()
    response = list(map(lambda row: (row[0], pickle.loads(row[1])), response))
    return response


@connect_bd
def get_area(id_area, connect=None):
    '''Return area(id, points) by id'''
    res = connect.execute('SELECT * FROM area WHERE id=?', [id_area])
    res = res.fetchall()
    if not res:
        raise sqlite3.DataError(f'Area with id={id_area} is not exists')
    return res[0]


@connect_bd
def add_courier(id_area, description, connect=None):
    '''Add new courier

    Keyword arguments:
    id_area -- area will be assigned to courier
    description -- info about courier
    '''
    # check there is area with id_area
    get_area(id_area)
    connect.execute('INSERT INTO courier VALUES(NULL, ?, ?)',
                    [id_area, description])
    connect.commit()


@connect_bd
def get_couriers_by_area(id_area, connect=None):
    '''Return couriers(list of (id_courier, id_area, description))
    who assigned to id_area'''
    res = connect.execute('SELECT * FROM courier WHERE id=?', [id_area])
    res = res.fetchall()
    if not res and not get_area(id_area):
        raise sqlite3.DataError(
            f'There are not couriers at this area({id_area})'
        )
    return res


@connect_bd
def get_all_couriers(connect=None):
    '''Return all couriers(list of (id_courier, id_area, description))'''
    return connect.execute('SELECT * FROM courier').fetchall()


@connect_bd
def clear_areas(connect=None):
    '''Delete all areas'''
    connect.execute('DELETE FROM area')


@connect_bd
def clear_couriers(connect=None):
    '''Delete all couriers'''
    connect.execute('DELETE FROM courier')


_init_tables()
