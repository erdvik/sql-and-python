import sqlite3
from numpy.random import uniform
import time

def main():
    task1 = Task1()
    difference = task1.compare_speed(task1.fill_table, task1.write_file)
    print(difference)

class Task1:
    #Filling a Table vs. Printing Values
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

if __name__ == "__main__":
    main()