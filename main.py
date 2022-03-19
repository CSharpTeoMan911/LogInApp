import mysql.connector
import PIL.Image
import io
import main
import sys

picture_binary_value = None
subject_index = 0


class Log_In_Or_Register_Database_Functionality:

    def __init__(self, username, password, log_in_or_register):

        try:
            if log_in_or_register == "Log In":
                self.Log_In(username, password)

            elif log_in_or_register == "Register":
                self.Register(username, password)

        except KeyboardInterrupt:
            sys.exit(0)

    def Register(self, username, password):

        try:
            if len(username) < 20 and len(password) < 20:
                con = mysql.connector.connect(user='student', password='User_Log_In',
                                              database='universityrecords', host='localhost')

                query = "INSERT INTO student_credentials(student_Id, student_password) VALUES(%s, %s)"

                parameters = (username, password)

                cursor = con.cursor()

                cursor.execute(query, parameters)

                con.commit()

                con.close()

                Log_In_Or_Register_Ui_Menu.main()

            else:
                print("\n\n\n\n! ! ! Username or password too long ! ! !")
                Log_In_Or_Register_Ui_Menu.main()


        except KeyboardInterrupt:
            sys.exit(0)

    def Log_In(self, username, password):

        try:
            con = mysql.connector.connect(user='student', password='User_Log_In',
                                          database='universityrecords', host='localhost')
            cursor = con.cursor()
            query = ("SELECT student_Id, "
                     "student_password FROM  "
                     "student_credentials ")

            cursor.execute(query)

            Correct_Credentials = False

            for student_Id, student_password in cursor:

                print("Loging in . . . ")

                if username == student_Id and student_password == password:
                    Correct_Credentials = True
                    App_Functionality_Ui_Menu(username)

            if Correct_Credentials is False:
                print("\n\n\n\n! ! ! Username, password or username and password are wrong ! ! !")
                Log_In_Or_Register_Ui_Menu().main()

        except KeyboardInterrupt:
            sys.exit(0)


class App_Functionality_Ui_Menu:

    def __init__(self, username):

        try:
            print("\n\n\n\n\n  ___________________")
            print(" / Application Menu /")
            print("-------------------\n\n\n\n\n")

            user_selection = input("Enter 'P' for profile, 'G' for grades, 'M' for materials, 'C' for contacts,  "
                                   "'L' to log out or 'E' to exit:  ")

            if user_selection == 'P':
                Profile_App_Functionality(username)

            elif user_selection == 'G':
                Grades_App_Functionality(username)

            elif user_selection == 'M':
                Materials_App_Functionality(username)

            elif user_selection == 'C':
                Contacts_App_Functionality(username)

            elif user_selection == 'L':
                Log_In_Or_Register_Ui_Menu.main()

            elif user_selection == 'E':
                main.Exit_Application()

            else:
                App_Functionality_Ui_Menu(username)


        except KeyboardInterrupt:
            sys.exit(0)




class Materials_App_Functionality:

    def __init__(self, username):

        try:
            con = mysql.connector.connect(user='student', password='User_Log_In',
                                          database='universityrecords', host='localhost')

            cursor = con.cursor()
            Query = None

            match main.subject_index:
                case 0:

                    print(" ___________________________")
                    print("|   Computer Systems        |")
                    print(" ---------------------------")

                    Query = ("SELECT material_name, Week_Value "
                             "FROM computer_systems_materials_foundation_year ")

                case 1:

                    print(" ___________________________")
                    print("|        Databases          |")
                    print(" ---------------------------")

                    Query = ("SELECT material_name, Week_Value "
                             "FROM databases_materials_year_1 ")

                case 2:

                    print(" ___________________________")
                    print("|    Foundation Project     |")
                    print(" ---------------------------")

                    Query = ("SELECT material_name, Week_Value "
                             "FROM foundation_project_materials_foundation_year ")

                case 3:

                    print(" ________________________________")
                    print("|   Fundamentals of Programming  |")
                    print(" --------------------------------")

                    Query = ("SELECT material_name, Week_Value "
                             "FROM fundamentals_of_programming_materials_foundation_year ")

                case 4:

                    print(" __________________________________________")
                    print("|   Fundamentals of software engineering   |")
                    print(" ------------------------------------------")

                    Query = ("SELECT material_name, Week_Value "
                             "FROM fundamentals_of_software_engineering_materials_year_1 ")

                case 5:

                    print(" __________________________________________")
                    print("|   Logical analysis and problem solving   |")
                    print(" ------------------------------------------")

                    Query = ("SELECT material_name, Week_Value "
                             "FROM logical_analysis_materials_foundation_year ")

            cursor.execute(Query)

            for material_name, Week_Value in cursor:

                if material_name is not None and Week_Value is not None:
                    print("\n\n\n\n\n\nMaterial name: ", material_name, "    Week: ", Week_Value)

            cursor.close()
            con.close()

            user_input = input("\n\n\n\n\nEnter 'N' to go to the next subject, 'P' to go to the previous"
                               " subject, 'D' to download a file, 'M' to go to the main menu, "
                               "'L' to log out or 'E' to exit:  ")

            if user_input == 'N':

                if main.subject_index < 5:

                    main.subject_index += 1
                    Materials_App_Functionality(username)

                else:
                    Materials_App_Functionality(username)


            elif user_input == 'P':

                if main.subject_index > 0:

                    main.subject_index -= 1
                    Materials_App_Functionality(username)

                else:
                    Materials_App_Functionality(username)


            elif user_input == 'D':

                match main.subject_index:
                    case 0:
                        self.File_Download("computer_systems_materials_foundation_year", username)

                    case 1:
                        self.File_Download("databases_materials_year_1", username)

                    case 2:
                        self.File_Download("foundation_project_materials_foundation_year", username)

                    case 3:
                        self.File_Download("fundamentals_of_programming_materials_foundation_year", username)

                    case 4:
                        self.File_Download("fundamentals_of_software_engineering_materials_year_1", username)

                    case 5:
                        self.File_Download("logical_analysis_materials_foundation_year", username)



            elif user_input == 'M':
                App_Functionality_Ui_Menu(username)

            elif user_input == 'L':
                Log_In_Or_Register_Ui_Menu().main()

            elif user_input == 'E':
                main.Exit_Application()

            else:
                Materials_App_Functionality(username)

        except KeyboardInterrupt:
            sys.exit(0)

    def File_Download(self, table_name, username):

        try:
            try:
                file_name = input("\n\n\n\nPlease enter the file name that you want to download: ")

                file_week = input("\n\n\n\nPlease enter the week of the file that you want to download: ")

                file_download_connection = mysql.connector.connect(user='student', password='User_Log_In',
                                                                   database='universityrecords', host='localhost')

                file_download_cursor = file_download_connection.cursor()

                file_download_query = (
                        "SELECT material_file FROM " + table_name + " WHERE material_name = '" + file_name + "' AND Week_Value ='" + file_week + "'")

                file_download_cursor.execute(file_download_query)

                material_file = file_download_cursor.fetchall()

                for i in material_file:
                    data = i[0]

                    with open(file_name, 'wb') as f:
                        print("\n\n\n\n Downloading . . . ")
                        f.write(data)

                Materials_App_Functionality(username)

            except:
                print("! ! ! Connection error ! ! !")
                Materials_App_Functionality(username)


        except KeyboardInterrupt:
            sys.exit(0)








class Contacts_App_Functionality:
    academic_institution_counter = 0

    def __init__(self, username):

        try:
            con = mysql.connector.connect(user='student', password='User_Log_In',
                                          database='universityrecords', host='localhost')
            cursor = con.cursor()

            query = ("SELECT * FROM"
                     " university_contacts")

            cursor.execute(query)

            print("\n\n ___________")
            print("/ Contacts /")
            print("-----------\n\n")

            for academic_institution, institution_landline_number, institution_email, institution_picture in cursor:
                self.academic_institution_counter += 1

                print("Academic institution ", str(self.academic_institution_counter), ": ",
                      academic_institution,
                      "\n\n", "Phone number: ", institution_landline_number, "\n\n",
                      "Email address: ", institution_email, "\n\n\n\n\n\n")

            user_input = input("Enter 'M' to go back to the main menu, 'V' to view the academic"
                               " institution's picture, 'L' to log out or 'E' to exit:  ")
            cursor.close()
            con.close()

            if user_input == 'M':
                App_Functionality_Ui_Menu(username)

            elif user_input == 'V':
                self.View_Accadimic_Institution_Picture(username)

            elif user_input == 'L':
                Log_In_Or_Register_Ui_Menu.main()

            elif user_input == 'E':
                main.Exit_Application()

            else:
                Contacts_App_Functionality(username)


        except KeyboardInterrupt:
            sys.exit(0)


    def View_Accadimic_Institution_Picture(self, username):

        academic_institution = input("\n\nEnter the academic institution's name:  ")

        con = mysql.connector.connect(user='student', password='User_Log_In',
                                      database='universityrecords', host='localhost')
        cursor = con.cursor()

        query = ("SELECT institution_picture "
                 "FROM"
                 " university_contacts "
                 "WHERE "
                 "academic_institution = '" + academic_institution + "'")

        cursor.execute(query)

        retrieved_institution_picture = cursor.fetchall()

        print("\n\n" + academic_institution + " profile picture:")

        for binary in retrieved_institution_picture:
            data = binary[0]
            institution_image = PIL.Image.open(io.BytesIO(data))
            institution_image.show()

        Contacts_App_Functionality(username)


class Grades_App_Functionality:

    def __init__(self, username):

        try:
            con = mysql.connector.connect(user='student', password='User_Log_In',
                                          database='universityrecords', host='localhost')

            cursor = con.cursor()
            Query = None

            match main.subject_index:
                case 0:
                    Query = ("SELECT Grade1, Grade2, Grade3 "
                             "FROM computer_systems_grades_foundation_year "
                             "WHERE student_Id =" + "'" + username + "'")

                case 1:
                    Query = ("SELECT Grade1, Grade2, Grade3 "
                             "FROM databases_grades_year_1 "
                             "WHERE student_Id =" + "'" + username + "'")

                case 2:
                    Query = ("SELECT Grade1, Grade2, Grade3 "
                             "FROM foundation_project_grades_foundation_year "
                             "WHERE student_Id =" + "'" + username + "'")

                case 3:
                    Query = ("SELECT Grade1, Grade2, Grade3 "
                             "FROM fundamentals_of_programming_grades_foundation_year "
                             "WHERE student_Id =" + "'" + username + "'")

                case 4:
                    Query = ("SELECT Grade1, Grade2, Grade3 "
                             "FROM fundamentals_of_software_engineering_grades_year_1 "
                             "WHERE student_Id =" + "'" + username + "'")

                case 5:
                    Query = ("SELECT Grade1, Grade2, Grade3 "
                             "FROM logical_analysis_grades_foundation_year "
                             "WHERE student_Id =" + "'" + username + "'")

            cursor.execute(Query)

            for (Grade1, Grade2, Grade3) in cursor:
                grade1 = Grade1
                grade2 = Grade2
                grade3 = Grade3

            match main.subject_index:
                case 0:
                    Query = ("SELECT FinalGrade "
                             "FROM computer_systems_final_grade_foundation_year "
                             "WHERE student_Id =" + "'" + username + "'")

                case 1:
                    Query = ("SELECT FinalGrade "
                             "FROM databases_final_grade_year_1 "
                             "WHERE student_Id =" + "'" + username + "'")

                case 2:
                    Query = ("SELECT FinalGrade "
                             "FROM foundation_project_final_grade_foundation_year "
                             "WHERE student_Id =" + "'" + username + "'")

                case 3:
                    Query = ("SELECT FinalGrade "
                             "FROM fundamentals_of_programming_final_grade_foundation_year "
                             "WHERE student_Id =" + "'" + username + "'")

                case 4:
                    Query = ("SELECT FinalGrade "
                             "FROM fundamentals_of_software_engineering_final_grade_year_1 "
                             "WHERE student_Id =" + "'" + username + "'")

                case 5:
                    Query = ("SELECT FinalGrade "
                             "FROM logical_analysis_final_grade_foundation_year "
                             "WHERE student_Id =" + "'" + username + "'")

            cursor.execute(Query)

            final_grade = cursor.fetchall()

            print(" ________________________________________________")

            match main.subject_index:
                case 0:
                    print("| Subject = Computer Systems                     |")
                case 1:
                    print("| Subject = Databases                            |")
                case 2:
                    print("| Subject = Foundation Project                   |")
                case 3:
                    print("| Subject = Fundamentals of Programming          |")
                case 4:
                    print("| Subject = Fundamentals of Software Engineering |")
                case 5:
                    print("| Subject = Logical Analysis and Problem Solving |")

            print("|________________________________________________|\n\n")
            print("\t\tGrade1 = ", grade1, "\n\n")
            print("\t\tGrade2 = ", grade2, "\n\n")
            print("\t\tGrade3 = ", grade3, "\n\n")

            cursor.close()
            con.close()

            if final_grade[0][0] is None:
                print("\t\tFinal Grade = N/A")

            else:
                print("\t\tFinal Grade = ", final_grade[0][0], "\n\n\n\n")

            user_input = input("\n\n\nEnter 'N' to select the next subject, 'P' to select the previous subject, "
                               "'M' to go back to the application's menu, 'L' to log out or 'E' to exit:  ")

            if user_input == "N":

                if main.subject_index < 5:

                    main.subject_index += 1
                    Grades_App_Functionality(username)

                else:
                    Grades_App_Functionality(username)

            elif user_input == "P":

                if main.subject_index > 0:

                    main.subject_index -= 1
                    Grades_App_Functionality(username)

                else:
                    Grades_App_Functionality(username)

            elif user_input == "M":

                main.subject_index = 0

                App_Functionality_Ui_Menu(username)

            elif user_input == "L":

                main.subject_index = 0

                Log_In_Or_Register_Ui_Menu.main()

            elif user_input == "E":
                main.Exit_Application()


            else:
                Grades_App_Functionality(username)

        except KeyboardInterrupt:
            sys.exit(0)




class Profile_App_Functionality:


    def __init__(self, username):

        try:
            con = mysql.connector.connect(user='student', password='User_Log_In',
                                          database='universityrecords', host='localhost')

            cursor = con.cursor()

            user_input = input("\n\n\n\nEnter 'V' to view the profile picture of the account, "
                               "'U' to upload a profile picture, "
                               "'M' to go back to the main menu, "
                               "'L' to log out or 'E' to exit:  ")

            if user_input == 'V':

                try:
                    query = ("SELECT student_profile_picture "
                             "FROM "
                             "student_credentials "
                             "WHERE "
                             "student_Id ='" + username + "';")

                    cursor.execute(query)

                    profile_picture = cursor.fetchall()

                    for i in profile_picture:
                        data = i[0]
                        img = PIL.Image.open(io.BytesIO(data))
                        img.show()

                    cursor.close()
                    con.close()

                except:
                    print()

                Profile_App_Functionality(username)

            elif user_input == 'U':
                file_path = input("\n\n\n\nInsert the picture's file path: ")

                try:
                    with open(file_path, "rb") as b:
                        data = b.read()
                except:
                    Profile_App_Functionality(username)

                try:
                    image_verifier = PIL.Image.open(io.BytesIO(data))
                    image_verifier.show()
                    image_verifier.close()
                except:
                    print('\n\n\n ! ! !The file inserted is not an image ! ! ! ')
                    Profile_App_Functionality(username)

                output = input("\n\n\n\nIs this the desired profile picture?\nEnter 'Y' for yes or 'N' for no:  ")

                if output == 'Y':

                    query = ("UPDATE student_credentials "
                             "SET  "
                             "student_profile_picture = %s "
                             "WHERE "
                             "student_Id = %s;")

                    parameters = (data, username)

                    cursor.execute(query, parameters)
                    con.commit()
                    con.close()
                    Profile_App_Functionality(username)

                elif output == 'N':
                    Profile_App_Functionality(username)

                else:
                    Profile_App_Functionality(username)




            elif user_input == 'M':
                App_Functionality_Ui_Menu(username)

            elif user_input == 'L':
                Log_In_Or_Register_Ui_Menu().main()

            elif user_input == 'E':
                main.Exit_Application()

            else:
                Profile_App_Functionality(username)

        except KeyboardInterrupt:
            sys.exit(0)


class Log_In_Or_Register_Ui_Menu:

    @staticmethod
    def main():
        try:
            print(" \n\n\n\n  _________________")
            print(" / Student Portal /")
            print(" -----------------\n\n\n\n\n")

            userinput = input("Enter 'L' to log in, 'R' to register or 'E' to exit:   ")

            if userinput == 'L':

                print("\n\n  _________")
                print(" / Log In /")
                print(" ---------\n\n")

                username = input("Enter your username:  ")
                password = input("Enter your password:  ")
                Log_In_Or_Register_Database_Functionality(username, password, "Log In")

            elif userinput == 'R':

                print("\n\n  ___________")
                print(" / Register /")
                print(" -----------\n\n")

                username = input("Enter your username:  ")
                password = input("Enter your password:  ")
                Log_In_Or_Register_Database_Functionality(username, password, "Register")


            elif userinput == 'E':
                main.Exit_Application()

            else:
                Log_In_Or_Register_Ui_Menu().main()


        except KeyboardInterrupt:
            sys.exit(0)



def Exit_Application():
    print("     ____________________________")
    print("    /                       / X /")
    print("   /_______________________/___/")
    print("  / The ' STUDENT PORTAL      /")
    print(" /  APPLICATION ' is closing /")
    print("/___________________________/")

    sys.exit(0)


if __name__ == '__main__':
    try:
        u = Log_In_Or_Register_Ui_Menu
        u.main()
    except KeyboardInterrupt:
        sys.exit(0)


