import pymysql
import pymysql.cursors
from auth_data import host, user, password, db_name


class DataBase:
    '''
    A class providing connection to database
    '''
    def add_note(self, us, home_adress, to_adress):
        '''
	Function adding note to database

        :param us: user_id of a user made a request
        :type us: str
        :param home_adress: first adress of a user made a request
        :type home_adress: str
        :param to_adress: second adress of a user made a request
        :type to_adress: str
        :return 0: Zero
        :rtype: int
        '''
        try:
            connect = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                database=db_name,
                password=password,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Connected")
            try:
                with connect.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO `users` (username, adress_from, adress_to) VALUES (%s, %s, %s)",
                        (us, home_adress, to_adress)
                    )
                    connect.commit()
                    print("Wrote a person")
            finally:
                connect.close()
        except Exception as ex:
            print(ex)
        return 0

    def get_notes_by_user(self, user_id):
        '''Function getting notes from db by userid

        :param user_id: user_id of a user made a request
        :type user_id: str
        :return res: Dictionary with distance, duration and screenshot
        :rtype: dict
       '''
        res = []
        try:
            connect = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                database=db_name,
                password=password,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Connected")
            try:
                with connect.cursor() as cursor:
                    select_all_rows = "SELECT * FROM `users`"
                    cursor.execute(select_all_rows)
                    rows = cursor.fetchall()
                    i = 1
                    for row in rows:
                        if str(row["username"]) == str(user_id):
                            res.append(f'{i}) From: {row["adress_from"]} to: {row["adress_to"]}')
                            i += 1
            finally:
                connect.close()
        except Exception as ex:
            print(ex)
        return res
