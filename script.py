import sqlite3
from numpy.random import uniform
import time

def main():
    task1 = Task1()
    diff_1 = task1.compare_speed(task1.fill_table, task1.write_file)
    print(diff_1)
    task2 = Task2()
    diff_2 = task1.compare_speed(task2.db_filtering_python, task2.db_filtering_sql)
    print(diff_2)


#Filling a Table vs. Printing Values
class Task1:
    def fill_table(self):
        random_numbers = uniform(low=10.0, high=25.0, size=100000)

        connection = sqlite3.connect("original.db")
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE Pressure (
                            reading float not null
                        );''')
        query = ''' INSERT INTO Pressure (reading)
                    VALUES (?);'''

        for number in random_numbers:
            cursor.execute(query, [number])
        
        cursor.close()
        connection.commit()
        connection.close()
    
    def write_file(self):
        random_numbers = uniform(low=10.0, high=25.0, size=100000)
        with open('random_numbers.txt', 'w') as outfile:
            for number in random_numbers:
                outfile.write("{}\n".format(number))

    def check_func_speed(self, func):
        start_time = time.time()
        func()
        end_time = time.time()
        return end_time - start_time

    def compare_speed(self, func1, func2):
        speed1 = self.check_func_speed(func1)
        speed2 = self.check_func_speed(func2)
        difference = speed1 - speed2
        string = "Function 1 took {speed1} seconds.\nFunction 2 took {speed2} seconds.\nThe difference is {difference} seconds".format(speed1=speed1, speed2=speed2, difference=difference)
        return string

#Filtering in SQL vs. Filtering in Python
class Task2:
    def db_filtering_python(self):
        connection_original = sqlite3.connect("original.db")
        cursor_original = connection_original.cursor()
        cursor_original.execute("SELECT * FROM Pressure;")
        results = cursor_original.fetchall()
        cursor_original.close()
        connection_original.close()

        connection_backup = sqlite3.connect("backup_py.db")
        cursor_backup = connection_backup.cursor()
        cursor_backup.execute('''CREATE TABLE Pressure (reading float not null);''')
        query = "INSERT INTO Pressure (reading) VALUES (?);"

        for entry in results:
            # number is saved in the first column of the table
            if entry[0] > 20.0:
                cursor_backup.execute(query, entry)

        cursor_backup.close()
        connection_backup.commit()
        connection_backup.close()

    def db_filtering_sql(self):
        connection_original = sqlite3.connect("original.db")
        cursor_original = connection_original.cursor()
        cursor_original.execute("SELECT * FROM Pressure WHERE reading > 20.0;")
        results = cursor_original.fetchall()
        cursor_original.close()
        connection_original.close()

        connection_backup = sqlite3.connect("backup_sql.db")
        cursor_backup = connection_backup.cursor()
        cursor_backup.execute("CREATE TABLE Pressure (reading float not null)")
        query = "INSERT INTO Pressure (reading) VALUES (?);"

        for entry in results:
            cursor_backup.execute(query, entry)

        cursor_backup.close()
        connection_backup.commit()
        connection_backup.close()





if __name__ == "__main__":
    main()