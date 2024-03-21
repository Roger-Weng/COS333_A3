#-----------------------------------------------------------------------
# database.py
# Authors: Roger Weng, Vishva Ilavelan
#-----------------------------------------------------------------------


import sqlite3
import contextlib
import sys

#-----------------------------------------------------------------------
# URL for database file
DATABASE_URL = 'file:reg.sqlite?mode=ro'

# search for specific classes with certain constraints
def search(dept, num, area, title):
    try:
        values = (escape_special_characters(dept),
                  escape_special_characters(num),
                  escape_special_characters(area),
                  escape_special_characters(title))
        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                stmt_str = "SELECT classid, dept, "
                stmt_str += "coursenum, area, title "
                stmt_str += "FROM courses, crosslistings, classes "
                stmt_str += "WHERE classes.courseid = courses.courseid "
                stmt_str += "AND crosslistings.courseid "
                stmt_str += "= courses.courseid "
                stmt_str += "AND dept LIKE ? ESCAPE '\\' "
                stmt_str += "AND coursenum LIKE ? ESCAPE '\\' "
                stmt_str += "AND area LIKE ? ESCAPE '\\' "
                stmt_str += "AND title LIKE ? ESCAPE '\\' "

                # add more AND statements here for all fields
                stmt_str += "ORDER BY dept, coursenum, classid "
                cursor.execute(stmt_str, [f"%{values[0]}%",
                                          f"%{values[1]}%",
                                          f"%{values[2]}%",
                                          f"%{values[3]}%"])
                table = cursor.fetchall()
                return_list = []
                return_list.append(True)
                classes_list = []

                for row in table:
                    class_dict = {"classid": row[0], "dept": row[1],
                                 "coursenum": row[2], 
                                 "area": row[3], "title": row[4]}
                    classes_list.append(class_dict)

                return_list.append(classes_list)
                return return_list

    except Exception as ex:
        return_list = []
        return_list.append(False)
        return_list.append(
"A server error occurred. Please contact the system administrator.")
        print(sys.argv[0] + ":", ex, file=sys.stderr)

        return return_list


# returns necessary data for class details query, based on a given
# classid
def get_class_details(classid_input):

    try:

        with sqlite3.connect(DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:

                stmt_str = "SELECT courseid, days, starttime, "
                stmt_str += "endtime, bldg, roomnum "
                stmt_str += "FROM classes WHERE classid = ? "
                cursor.execute(stmt_str, [classid_input])
                class_table = cursor.fetchall()
                if len(class_table) == 0:
                    print(sys.argv[0]+":", "no class with classid",
                    classid_input, "exists", file=sys.stderr)
                    return_list = [False]
                    return_list.append(
        "no class with classid " + str(classid_input) + " exists")

                    return return_list

                row = class_table[0]
                course_id = row[0]

                class_dict = {"courseid": course_id, "days": row[1],
                             "starttime": row[2],
                             "endtime": row[3],
                             "bldg": row[4], "roomnum": row[5]}

                stmt_str = "SELECT dept, coursenum "
                stmt_str += "FROM crosslistings WHERE courseid = ? "
                stmt_str += "ORDER BY dept, coursenum "
                cursor.execute(stmt_str, [course_id])
                dept_table = cursor.fetchall()

                deptcoursenums_list = []
                for row in dept_table:
                    deptcoursenums_list.append([row[0], row[1]])
                class_dict["deptcoursenums"] = deptcoursenums_list

                stmt_str = "SELECT area, title, descrip, prereqs "
                stmt_str += "FROM courses WHERE courseid = ? "
                cursor.execute(stmt_str, [course_id])
                course_table = cursor.fetchall()

                row = course_table[0]
                class_dict["area"] = row[0]
                class_dict["title"] = row[1]
                class_dict["descrip"] = row[2]
                class_dict["prereqs"] = row[3]

                stmt_str = "SELECT profname "
                stmt_str += "FROM coursesprofs, profs "
                stmt_str += "WHERE courseid = ? "
                stmt_str += "AND profs.profid = coursesprofs.profid "
                stmt_str += "ORDER BY profname "

                cursor.execute(stmt_str, [course_id])

                prof_table = cursor.fetchall()

                profs_list = []
                for row in prof_table:
                    profs_list.append(row[0])

                class_dict["profnames"] = profs_list

                return_list = [True]
                return_list.append(class_dict)
                return return_list

    except Exception as ex:
        return_list = []
        return_list.append(False)
        return_list.append(
"A server error occurred. Please contact the system administrator.")

        print(sys.argv[0] + ":", ex, file=sys.stderr)

        return return_list


def escape_special_characters(string):
    return string.replace('_', '\\_').replace('%', '\\%')
