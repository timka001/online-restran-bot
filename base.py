import sqlite3
from sqlite3 import Error



def SavatDelete(user_id):
    try:
        connection = sqlite3.connect('DataBase.db')
        cursor = connection.cursor()
        sqlite_select_query = f"DELETE FROM Savat WHERE user_id='{user_id}';"
        cursor.execute(sqlite_select_query)
        connection.commit()
        cursor.close()
    except (Exception, Error) as eror:
        print(f"xato {eror}")
    finally:
        if connection:
            connection.close()






def SavatRead(user_id):
    try:
        connection = sqlite3.connect('DataBase.db')
        cursor = connection.cursor()
        sqlite_select_query = f"select * from Savat where user_id='{user_id}'"
        cursor.execute(sqlite_select_query)
        totalRows = cursor.fetchall()
        cursor.close()
        return totalRows
    except (Exception, Error) as eror:
        print(f"xato {eror}")
    finally:
        if connection:
            connection.close()




def InsertSavat(user_id, taom, soni, narxi):
    try:
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("""Insert into Savat(user_id, taom, soni, narxi) values(?, ?, ?, ?)""",(user_id, taom, soni, narxi))
        connection.commit()
        cursor.close()
    except (Exception, Error) as eror:
        print(f"xato {eror}")
    finally:
        if connection:
            connection.close()


















def CreateBasket():
    try:
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("""
        Create table Savat(
            id INTEGER  PRIMARY KEY not null,
            user_id int not null,
            taom text not null,
            soni integer not null,
            narxi  real not null
                       );""")
        connection.commit()
        cursor.close()
    except (Exception, Error) as eror:
        print(f"xato {eror}")
    finally:
        if connection:
            connection.close()
            print("tugadi")













def TaomRead(name):
    try:
        connection = sqlite3.connect('DataBase.db')
        cursor = connection.cursor()
        sqlite_select_query = f"select * from Product where foodname='{name}'"
        cursor.execute(sqlite_select_query)
        totalRows = cursor.fetchall()
        cursor.close()
        return totalRows
    except (Exception, Error) as eror:
        print(f"xato {eror}")
    finally:
        if connection:
            connection.close()





def ProductRead(cat_id):
    try:
        connection = sqlite3.connect('DataBase.db')
        cursor = connection.cursor()
        sqlite_select_query = f"select * from Product where category_id={cat_id}"
        cursor.execute(sqlite_select_query)
        totalRows = cursor.fetchall()
        cursor.close()
        return totalRows
    except (Exception, Error) as eror:
        print(f"xato {eror}")
    finally:
        if connection:
            connection.close()














def CategoryRead():
    try:
        connection = sqlite3.connect('DataBase.db')
        cursor = connection.cursor()
        sqlite_select_query = """SELECT * from Category"""
        cursor.execute(sqlite_select_query)
        totalRows = cursor.fetchall()
        cursor.close()
        return totalRows
    except (Exception, Error) as eror:
        print(f"xato {eror}")
    finally:
        if connection:
            connection.close()



def InsertCategory(id, name):
    try:
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Category(id, name) VALUES (?, ?)",(id, name))
        connection.commit()
        cursor.close()
    except (Exception, Error) as eror:
        print(f"xato {eror}")
    finally:
        if connection:
            connection.close()




def InsertProduct(cat_id, price, food, image):
    try:
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("""Insert into Product(category_id, price, foodname, image) values(?, ?, ?, ?)""",(cat_id, price, food, image))
        connection.commit()
        cursor.close()

    except (Exception, Error) as eror:
        print(f"xato {eror}")
    finally:
        if connection:
            connection.close()


def CreateProduct():
    try:
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("""
        Create table Product(
            id INTEGER  PRIMARY KEY not null,
            category_id int not null,
            price real not null,
            foodname text not null,
            image text not null
                       );""")
        connection.commit()
        cursor.close()
        print("bajarildi")
    except (Exception, Error) as eror:
        print(f"xato {eror}")
    finally:
        if connection:
            connection.close()
            print("tugadi")






def CreateCategory():
    try:
        connection = sqlite3.connect("DataBase.db")
        cursor = connection.cursor()
        cursor.execute("""
        Create table Category(
            ID INTEGER PRIMARY KEY NOT NULl,
            name text not null
                       );""")
        connection.commit()
        cursor.close()
        print("bajarildi")
    except (Exception, Error) as eror:
        print(f"xato {eror}")
    finally:
        if connection:
            connection.close()
            print("tugadi")