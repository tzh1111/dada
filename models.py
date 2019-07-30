# models.py
from werkzeug.security import generate_password_hash
import datetime
from flask_login import UserMixin
from dada_db import Mysql
import time as tm
import uuid
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError


class Relation_control():
    def __init__(self):
        self.exsist = True

    def initialize_request(self, user_id, group_id):
        sql = Mysql()
        info = []
        time1 = tm.time()
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        info.append(user_id)
        info.append(group_id)

        result = sql.multiple_select("*", "ismember", "group_ID", group_id, "user_ID", user_id)
        if result:
            info.append("is_mem")
        else:
            info.append("no_mem")

        try:  # should use mysql, but just profile_file here...
            if info[2] == "is_mem":
                info.append("already_in")
                info.append(str(int(time1)))
                info.append(time)
            else:
                info.append("ready_to_apply")
                info.append(str(int(time1)))
                info.append(time)
            sql.insert_requirement("wanttojoin", info)
            print("success!\n")
            sql.disconnect()
            return
        except IOError:
            return None
        except ValueError:
            return None

    def check_request(self, user_id, group_id):
        sql = Mysql()
        info = []

        try:  # should use mysql, but just profile_file here...
            result = sql.multiple_select("*", "wanttojoin", "group_ID", group_id, "user_ID", user_id)
            sql.disconnect()
            if result:
                return True
            else:
                self.initialize_request(user_id, group_id)
            return
        except IOError:
            return None
        except ValueError:
            return None

    def show_deal_request(self, user_id):
        sql = Mysql()
        info = []

        try:  # should use mysql, but just profile_file here...
            result1 = sql.select("group_ID", "group_s", "user_ID", user_id)
            # print(result1)
            if result1:
                for row in result1:
                    group_id = row[0]
                    result2 = sql.multiple_select_2("*", "wanttojoin", "group_ID", group_id, "status", "no_mem",
                                                    "status2", "send_request")
                    print(result2)
                    for row1 in result2:
                        if row1[1] == group_id:
                            record = {}
                            # messages = [{'id': 'message1', 'when': '2019-09-28', 'who': 'a', 'which': 'group1'}]
                            record["id"] = row1[4]
                            record["when"] = row1[5]
                            record["who"] = row1[0]
                            record["which"] = row1[1]
                            info.append(record)
                sql.disconnect()
                return info
            else:
                sql.disconnect()
                return []
        except IOError:
            return None
        except ValueError:
            return None

    def deal_request(self, status, request_id):
        sql = Mysql()

        try:
            if status == "accept":
                result = sql.select("*", "wanttojoin", "request_ID", request_id)
                sql.delete("wanttojoin", "request_ID", request_id)
                for row in result:
                    info = []
                    info.append(row[0])
                    info.append(row[1])
                    sql.insert_group("ismember", info)
                sql.disconnect()
            else:
                sql.delete("wanttojoin", "request_ID", request_id)
                sql.disconnect()
            return
        except IOError:
            return None
        except ValueError:
            return None

    def update_request(self, user_id, group_id, time):
        sql = Mysql()
        record = {}

        try:
            result = sql.multiple_select("status, status2", "wanttojoin", "group_ID", group_id, "user_ID", user_id)
            for row in result:
                if row[0] == "already_in":
                    print("alright")
                elif row[1] == "ready_to_apply":
                    sql.update("wanttojoin", "status2", "send_request", "group_ID", group_id, "user_ID", user_id)
                    sql.update("wanttojoin", "time", time, "group_ID", group_id, "user_ID", user_id)
                elif row[1] == "send_request":
                    sql.update("wanttojoin", "status2", "ready_to_apply", "group_ID", group_id, "user_ID", user_id)
                    sql.update("wanttojoin", "time", time, "group_ID", group_id, "user_ID", user_id)

            result = sql.multiple_select("*", "wanttojoin", "group_ID", group_id, "user_ID", user_id)
            for row in result:
                record["name"] = row[1]
                record["description"] = row[0] + " want to join it!"
                if row[2] == "is_mem":
                    record["status"] = "0"
                elif row[3] == "ready_to_apply":
                    record["status"] = "2"
                elif row[3] == "send_request":
                    record["status"] = "1"
            return record
        except IOError:
            return None
        except ValueError:
            return None

    def show_request(self, user_id):
        sql = Mysql()
        info = []

        try:
            result = sql.select("*", "wanttojoin", "user_ID", user_id)
            for row in result:
                record = {}
                record["name"] = row[1]
                record["description"] = row[0] + " want to join it!"
                if row[2] == "is_mem":
                    record["status"] = "0"
                elif row[3] == "ready_to_apply":
                    record["status"] = "2"
                elif row[3] == "send_request":
                    record["status"] = "1"
                info.append(record)
            return info
        except IOError:
            return None
        except ValueError:
            return None


class Friend_control():
    def __init__(self):
        self.exsist = True

    def check_relation(self, user_id, friend_id):
        sql = Mysql()

        try:
            result = sql.multiple_select("*", "isfriend", "use_user_ID", user_id, "user_ID", friend_id)
            sql.disconnect()
            if result:
                print("ignore")
            else:
                self.insert_friend(user_id, friend_id)
            return
        except IOError:
            return None
        except ValueError:
            return None

    def show_relation(self, user_id):
        sql = Mysql()
        info = []

        try:
            result = sql.select("*", "isfriend", "use_user_ID", user_id)
            for row in result:
                record = {}
                id1 = row[1]
                record["ID"] = id1
                result1 = sql.select("*", "users", "user_ID", id1)
                for row1 in result1:
                    record["name"] = row1[0]
                record["icon"] = ord(id1[-1]) % 3
                record["description"] = "i am a piggy!"
                info.append(record)
            sql.disconnect()
            return info
        except IOError:
            return None
        except ValueError:
            return None

    def insert_friend(self, user_id, friend_id):
        sql = Mysql()
        info = []

        info.append(user_id)
        info.append(friend_id)

        try:  # should use mysql, but just profile_file here...
            sql.insert_group("isfriend", info)
            print("success!\n")
            sql.disconnect()
            return
        except IOError:
            return None
        except ValueError:
            return None

    def delete_friend(self, user_id, friend_id):
        sql = Mysql()

        try:  # should use mysql, but just profile_file here...
            sql.delete_2("isfriend", "use_user_ID", user_id, "user_ID", friend_id)
            print("success!\n")
            sql.disconnect()
            return
        except IOError:
            return None
        except ValueError:
            return None

    def friend_count(self, user_id):
        sql = Mysql()
        info = []

        try:
            result = sql.select("*", "isfriend", "use_user_ID", user_id)
            print(result)
            for row in result:
                record = {}
                id1 = row[1]
                record["ID"] = id1
                info.append(record)
            sql.disconnect()
            return info
        except IOError:
            return None
        except ValueError:
            return None


class Comment():
    def __init__(self):
        self.exsist = True

    def create_dialog(self, diary_id, user_id, time, content):
        sql = Mysql()
        info = []
        time1 = tm.time()

        info.append(str(int(time1)))
        info.append(user_id)
        info.append(diary_id)
        info.append(time)
        info.append(content)

        try:  # should use mysql, but just profile_file here...
            sql.insert_dialog("comments", info)
            print("success!\n")
            sql.disconnect()
            return
        except IOError:
            return None
        except ValueError:
            return None

    def show_group_dialog(self, diary_id):
        sql = Mysql()
        info = []

        try:
            result = sql.join_select("comment_ID, users.user_ID, record_ID, date, content, username",
                                     "users", "comments", "user_ID", "record_ID", diary_id)
            print("success!\n")
            sql.disconnect()
            for row in result:
                record = {}
                record["comment_ID"] = row[0]
                cur_id = row[1]
                record["icon"] = ord(cur_id[-1]) % 3
                record["autherID"] = row[1]
                record["record_ID"] = row[2]
                record["date"] = row[3]
                record["content"] = row[4]
                record["authername"] = row[1]
                info.append(record)
            return info
        except IOError:
            return None
        except ValueError:
            return None


class Dialog():
    def __init__(self):
        self.exsist = True

    def create_dialog(self, group_id, user_id, time, content):
        sql = Mysql()
        info = []
        time1 = tm.time()

        info.append(str(int(time1)))
        info.append(group_id)
        info.append(user_id)
        info.append(time)
        info.append(content)

        try:  # should use mysql, but just profile_file here...
            sql.insert_dialog("dialog", info)
            print("success!\n")
            sql.disconnect()
            return
        except IOError:
            return None
        except ValueError:
            return None

    def show_group_dialog(self, group_id):
        sql = Mysql()
        info = []

        try:
            result = sql.select("*", "dialog", "group_ID", group_id)
            print("success!\n")
            sql.disconnect()
            for row in result:
                record = {}
                cur_id = row[2]
                record["mem"] = row[2]
                record["time"] = row[3]
                record["msg"] = row[4]
                record["icon"] = ord(cur_id[-1]) % 3
                info.append(record)
            return info
        except IOError:
            return None
        except ValueError:
            return None


class Group():
    def __init__(self):
        self.exsist = True

    def create_group(self, user_id, group_id):
        sql = Mysql()
        info = []
        # self.group_id = group_id
        # self.owner = user_id
        info.append(group_id)
        info.append(user_id)

        try:  # should use mysql, but just profile_file here...
            sql.insert_group("group_s", info)
            print("success!\n")
            sql.disconnect()
            return
        except IOError:
            return None
        except ValueError:
            return None

    def show_group_own(self, user_id):
        sql = Mysql()
        info = []

        try:
            result = sql.select("*", "group_s", "user_ID", user_id)
            print("success!\n")
            sql.disconnect()
            for row in result:
                record = {}
                record["name"] = row[0]
                record["description"] = row[1]
                info.append(record)
            return info
        except IOError:
            return None
        except ValueError:
            return None

    def show_group_join(self, user_id):
        sql = Mysql()
        info = []

        try:
            result = sql.select("*", "ismember", "user_ID", user_id)
            print("success!\n")
            for row in result:
                record = {}
                record["name"] = row[1]
                group_id = row[1]
                result1 = sql.select("*", "group_s", "group_ID", group_id)
                for row1 in result1:
                    record["description"] = row1[1]
                info.append(record)
            sql.disconnect()
            return info
        except IOError:
            return None
        except ValueError:
            return None

    def search_group(self, group_ID):
        sql = Mysql()
        info = []

        try:
            result = sql.blurry_select("*", "group_s", "group_ID", group_ID)
            print("success!\n")
            sql.disconnect()
            for row in result:
                record = {}
                record["name"] = row[0]
                record["description"] = row[1]
                record["status"] = "1"
                info.append(record)
            return info
        except IOError:
            return None
        except ValueError:
            return None

    def show_member(self, user_id, group_ID):
        sql = Mysql()
        info = []

        try:
            result = sql.select("*", "ismember", "group_ID", group_ID)
            for row in result:
                record = {}
                id1 = row[0]
                print(id1)
                record["ID"] = id1
                result1 = sql.multiple_select("*", "isfriend", "use_user_ID", user_id, "user_ID", id1)
                if result1:
                    record["isfriend"] = "1"
                else:
                    record["isfriend"] = "0"
                record["icon"] = ord(id1[-1]) % 3
                result2 = sql.select("*", "users", "user_ID", id1)
                for row1 in result2:
                    record["name"] = row1[0]
                info.append(record)
            sql.disconnect()
            print("success!\n")
            return info
        except IOError:
            return None
        except ValueError:
            return None

    def delete_quit_group(self, user_id, group_ID):
        sql = Mysql()
        flag = 0

        try:
            result = sql.select("*", "group_s", "user_ID", user_id)
            for row in result:
                if row[1] == str(user_id):
                    sql.delete("group_s", "group_ID", group_ID)
                    flag = 1
            if flag == 0:
                sql.delete("ismember", "user_ID", user_id)
            print("success!\n")
            sql.disconnect()
            return
        except IOError:
            return None
        except ValueError:
            return None


class Record():
    def __init__(self, user_email):
        self.user = user_email

    def create_new_record(self, time, content):
        sql = Mysql()
        info = []
        time1 = tm.time()

        info.append(str(int(time1)))
        info.append(self.user)
        info.append(time)
        info.append(content)

        try:  # should use mysql, but just profile_file here...
            sql.insert_record("records", info)
            print("success!\n")
            sql.disconnect()
            return
        except IOError:
            return None
        except ValueError:
            return None

    def display(self):
        sql = Mysql()
        content = []

        try:
            result = sql.select("*", "records", "user_ID", self.user)
            print(result)
            sql.disconnect()
            for row in result:
                record = {}
                record["ID"] = row[0]
                cur_id = row[1]
                record["icon"] = ord(cur_id[-1]) % 3
                record["user_id"] = row[1]
                record["time"] = row[2]
                record["content"] = row[3]
                content.append(record)
            return content
        except:
            return None

    def display_single(self, diary_id):
        sql = Mysql()
        try:
            content = []
            result = sql.select("*", "records", "record_ID", diary_id)
            sql.disconnect()
            for row in result:
                record = {}
                U_id = row[1]
                record["ID"] = row[0]
                record["user_id"] = row[1]
                record["icon"] = ord(U_id[-1]) % 3
                record["time"] = row[2]
                record["content"] = row[3]
                content.append(record)
            return content
        except:
            return None



class User(UserMixin):
    def __init__(self, user_email):
        self.user_email = user_email
        # self.username = username
        # self.password =
        # self.sex = self.get_sex()
        # self.birthday =
        self.id = self.get_id()
        # self.password = self.get_password_hash()


    '''
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """save user name, id and password hash to json file"""
        self.password_hash = generate_password_hash(password)
        with open(PROFILE_FILE, 'w+') as f:
            try:
                profiles = json.load(f)
            except ValueError:
                profiles = {}
            profiles[self.username] = [self.password_hash,
                                       self.id]
            f.write(json.dumps(profiles))
    '''
    # def get_sex(self):
    def save_password(self, password):
        self.password = generate_password_hash(password=password)

    def show_info(self):
        sql = Mysql()
        record = {}

        try: #should use mysql, but just profile_file here...
            result = sql.select("*", "users", "user_ID", self.user_email)
            sql.disconnect()
            for row in result:
                record["ID"] = row[0]
                record["name"] = row[2]
                record["others"] = "haha"
            return record
        except IOError:
            return None
        except ValueError:
            return None

    def insert_info(self, username, sex, birthday):
        sql = Mysql()
        info = []
        # self.password = self.password.split(":")[2]
        info.append(self.user_email)
        info.append(self.id)
        info.append(username)
        info.append(self.password)
        info.append(sex)
        info.append(birthday)
        try: #should use mysql, but just profile_file here...
            sql.insert("users", info)
            print("success!\n")
            sql.disconnect()
            return
        except IOError:
            return None
        except ValueError:
            return None
    '''
    def verify_password(self, password):
        # password_hash = self.get_password_hash()
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)
    '''

    def get_password_hash(self):
        """try to get password hash from file.

        :return password_hash: if the there is corresponding user in
                the file, return password hash.
                None: if there is no corresponding user, return None.
        """
        sql = Mysql()
        # sql.select(self.username)
        try: #should use mysql, but just profile_file here...
            password = []
            result = sql.select("password", "users", "user_ID", self.user_email)
            sql.disconnect()
            for row in result:
                password.append(row[0])
                self.password_check = password[0]
                return True
            else:
                print("wrong!\n")
                return False
        except IOError:
            return None
        except ValueError:
            return None

    def get_id(self):
        """get user id from profile file, if not exist, it will
        generate a uuid for the user.
        """
        if self.user_email is not None:
            sql = Mysql()
            try:
                id = []
                result = sql.select("user_sysid", "users", "user_ID", self.user_email)
                sql.disconnect()
                for row in result:
                    id.append(row[0])
                    return id[0]
            except IOError:
                pass
            except ValueError:
                pass
        return str(uuid.uuid4())

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not user_id:
            return None
        sql = Mysql()
        try:
            name = []
            result = sql.select("user_ID", "users", "user_sysid", user_id)
            sql.disconnect()
            for row in result:
                name.append(row[0])
                return User(name[0])
        except:
            return None
        return None
