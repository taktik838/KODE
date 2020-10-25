import sqlite3
import pickle

HOST = 'database.db'


def connect_bd(fun):
    def decorate(*args, **kwargs):
        with sqlite3.connect(HOST) as connect:
            return fun(connect, *args, **kwargs)
    return decorate

@connect_bd
def _init_tables(connect):
    connect.execute('''CREATE TABLE IF NOT EXISTS area (
                    id INTEGER PRIMARY KEY NOT NULL,
                    points NOT NULL
                    )''')

    connect.execute('''CREATE TABLE IF NOT EXISTS courier (
                    id INTEGER PRIMARY KEY NOT NULL,
                    area INTEGER NOT NULL,
                    description
                    )''')

    # connect.execute('''CREATE TABLE IF NOT EXISTS order (
    #                 id INTEGER PRIMARY KEY NOT NULL,
    #                 status NOT NULL,
    #                 delivery_coordinate NOT NULL
    #                 )''')


@connect_bd
def add_area(connect, points):
    connect.execute('INSERT INTO area VALUES(NULL, ?)', [pickle.dumps(points)])
    connect.commit()
    
@connect_bd
def add_areas(connect, areas):
    dump_areas = [(pickle.dumps(points),) for points in areas]
    connect.executemany('INSERT INTO area VALUES(NULL, ?)', dump_areas)
    connect.commit()
    
@connect_bd
def get_all_areas(connect):
    response = connect.execute('SELECT * FROM area').fetchall()
    response = list(map(lambda row: (row[0], pickle.loads(row[1])), response))
    return response

@connect_bd
def get_area(connect, id_area):
    res = connect.execute('SELECT * FROM area WHERE id=?', [id_area]).fetchall()
    if res:
        return res[0]
    else:
        raise sqlite3.DataError(f'Area with id={id_area} is not exists')

@connect_bd
def add_courier(connect, id_area, description):
    area = get_area(id_area)
    connect.execute('INSERT INTO courier VALUES(NULL, ?, ?)', [id_area, description])
    connect.commit()
    
@connect_bd
def get_couriers_by_area(connect, id_area):
    res = connect.execute('SELECT * FROM courier WHERE id_area=?', [id_area])
    if res:
        return res
    else:
        if not get_area(id_area):
            raise sqlite3.DataError(f'There are not couriers at this area({id_area})')
        

_init_tables()