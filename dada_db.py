from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pymysql

# db = SQLAlchemy()

'''
class Grade(db.Model):
    g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(20), unique=True)
    g_create_time = db.Column(db.DateTime, default=datetime.now)
    students = db.relationship('Student',backref= 'grade')

    __tablename__ = 'grade'

    def __init__(self, name):
        self.g_name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
'''

class Mysql:
    def __init__(self):
        self.db, self.cursor = self.connect()

    def connect(self):
        db = pymysql.connect(host='127.0.0.1', port=3306,
                             user='root', passwd='qwerty1601', db='dada', charset='utf8')
        cursor = db.cursor()
        return db, cursor

    def disconnect(self):
        self.db.close()

    def select(self, goal, table, col, item):#降序排序
        # to fill
        query = "select " + str(goal) + " from " + str(table) + " where " + str(col) + " = '" + str(item) + "'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def multiple_select(self, goal, table, col, item, col2, item2):#降序排序
        # to fill
        query = "select " + str(goal) + " from " + str(table) + " where " + str(col) + " = '" + str(item) + "'" + \
                " and " + str(col2) + " = '" + str(item2) + "'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def multiple_select_2(self, goal, table, col, item, col2, item2, col3, item3):#降序排序
        # to fill
        query = "select " + str(goal) + " from " + str(table) + " where " + str(col) + " = '" + str(item) + "'" + \
                " and " + str(col2) + " = '" + str(item2) + "'" + " and " + str(col3) + " = '" + str(item3) + "'"
        # print(query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def blurry_select(self, goal, table, col, item):#降序排序
        # to fill
        query = "select " + str(goal) + " from " + str(table) + " where " + str(col) + " like '%" + str(item) + "%'"
        # print(query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def join_select(self, goal, table1, table2, index, col, item):#降序排序
        # to fill
        query = "select " + str(goal) + " from " + str(table1) + ", " + str(table2) + " where " \
                + str(table1) + "." + str(index) + " = " + str(table2) + "." + str(index) + " and " \
                + str(col) + " = '" + str(item) + "'"
        # print(query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def insert(self, tablename, value):
        # to fill
        query = "insert into " + str(tablename) + " values( '" \
                + value[0] + "','" + value[1] + "','" + value[2] + "','"\
                + value[3] + "','" + value[4] + "','" + value[5] + "');"
        # print(query)
        try:
            self.cursor.execute(query)
            self.db.commit()
            # result = self.cursor.fetchall()
            return
        except:
            print("insert error")
            #handle()
        return

    def insert_group(self, tablename, value):
        # to fill
        query = "insert into " + str(tablename) + " values( '" \
                + value[0] + "','" + value[1] + "');"
        # print(query)
        try:
            self.cursor.execute(query)
            self.db.commit()
            # result = self.cursor.fetchall()
            return
        except:
            print("insert error")
            #handle()
        return

    def insert_dialog(self, tablename, value):
        # to fill
        query = "insert into " + str(tablename) + " values( '" \
                + value[0] + "','" + value[1] + "','" + value[2] + "','"\
                + value[3] + "','" + value[4] + "');"
        # print(query)
        try:
            self.cursor.execute(query)
            self.db.commit()
            # result = self.cursor.fetchall()
            return
        except:
            print("insert error")
            #handle()
        return

    def insert_record(self, tablename, value):
        # to fill
        query = "insert into " + str(tablename) + " values( '" \
                + value[0] + "','" + value[1] + "','" + value[2] + "','"\
                + value[3] + "');"
        # print(query)
        try:
            self.cursor.execute(query)
            self.db.commit()
            # result = self.cursor.fetchall()
            return
        except:
            print("insert error")
            #handle()
        return

    def insert_requirement(self, tablename, value):
        # to fill
        query = "insert into " + str(tablename) + " values( '" \
                + value[0] + "','" + value[1] + "','" + value[2] + "','" + \
                value[3] + "','" + value[4] + "','" + value[5] + "');"
        # print(query)
        try:
            self.cursor.execute(query)
            self.db.commit()
            # result = self.cursor.fetchall()
            return
        except:
            print("insert error")
            #handle()
        return

    def delete(self, tablename, constraint, con):
        # to fill
        query = "delete from " + str(tablename) + " where " + str(constraint) + " = '" + str(con) + "';"
        try:
            self.cursor.execute(query)
            self.db.commit()
        except:
            print("delete error")
            #handle()
        return

    def delete_2(self, tablename, constraint, con, constraint2, con2):
        # to fill
        query = "delete from " + str(tablename) + " where " + str(constraint) + " = '" + str(con) + "' and " + \
                str(constraint2) + " = '" + str(con2) + "';"
        try:
            self.cursor.execute(query)
            self.db.commit()
        except:
            print("delete error")
            #handle()
        return

    def update(self, tablename, up_col, up_data, con_col, con_data, con_col2, con_data2):
        # to fill
        query = "update " + str(tablename) + " set " + str(up_col) + " = '" + str(up_data) \
        + "' where " + str(con_col) + " = '" + str(con_data) + "' and " + str(con_col2) + \
        " = '" + str(con_data2) + "';"
        try:
            self.cursor.execute(query)
            self.db.commit()
        except:
            print("delete error")
            #handle()
        return

