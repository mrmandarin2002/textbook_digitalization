import socket
from tkinter import messagebox

class Client:

    # initialization method
    def __init__(self, address, port):

        # define server address
        self.server_address = (address, port)

        # initialize udp socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(("", 7357))
        self.udp_socket.settimeout(1)

    # method to close the udp socket
    def close(self):
        self.udp_socket.close()

    # basic data echo method
    def echo(self, msg):
        self.udp_socket.sendto(msg.encode("utf-8"), self.server_address)
        try: # try to receive data back from the server
            data = self.udp_socket.recvfrom(4096)[0]
            return data.decode("utf-8") # return decoded data
        except: # if a timeout exception was thrown
            messagebox.showerror("Connection Error", "Server is not connected")
            return "_"

    # command method
    def command(self, cmd, args):
        # only loop through the arguments array if there is at least one argument
        if len(args) > 0:
            # create initial message string, including the first element of the arguments list
            msg = cmd+";"+args[0]
            # add remaining elements of the arguments array
            if len(args) > 1:
                for arg in args[1:]:
                    msg += "|"+arg
            # return the response of the fully formed message string
            return self.echo(msg)
        else:
            return self.echo(cmd+";")

    # ping method (returns true if the server responds in less than one second)
    def ping(self):
        if self.command("p", []) == "1":
            return True
        else:
            return False

    # student id validation method
    def valid_s(self, student_id):
        if self.command("valid_s", [student_id]) == "1":
            return True
        else:
            return False

    # get student information
    def info_s(self, student_id):
        return self.command("info_s", [student_id]).split("|")

    # delete a textbook from the database
    def delete_t(self, textbook_id):
        return self.command("delete_t", [textbook_id])

    # add a textbook to the database
    def add_t(self, textbook_id, textbook_name, textbook_price, textbook_condition):
        return self.command("add_t", [textbook_id, textbook_name, textbook_price, textbook_condition])

    # add a student to the database
    def add_s(self, student_id, student_name, student_deposit):
        return self.command("add_s", [student_id, student_name, student_deposit])

    # get student textbooks from the database
    def student_t(self, student_id):
        value = self.command("student_t", [student_id]).split("|")
        if value[0] == "":
            return []
        else:
            return value

    # textbook id validation method
    def valid_t(self, textbook_id):
        if self.command("valid_t", [textbook_id]) == "1":
            return True
        else:
            return False

    # get textbook information from the database
    def info_t(self, textbook_id):
        return self.command("info_t", [textbook_id]).split("|")

    # assign textbook to student in database
    def assign_t(self, textbook_id, student_id):
        return self.command("assign_t", [textbook_id, student_id])

    # retun textbook from student in database
    def return_t(self, textbook_id):
        return self.command("return_t", [textbook_id])

    # get a list of all course numbers
    def courses_n(self):
        return self.command("courses_n", []).split("|")

    # get a list of requisite textbooks for a given course
    def course_r(self, course_id):
        return self.command("course_r", [course_id]).split("|")

    # get course information for a given course
    def info_c(self, course_id):
        return self.command("info_c", [course_id]).split("~")
    
    # sets the requisite textbooks for a course
    def set_course_r(self, course_id, course_r):
        return self.command("set_course_r", [course_id, "~".join(course_r)])
    
    # gets a list of teacher names
    def get_teachers(self):
        return self.command("get_teachers", []).split("|")
    
    # gets the list of courses for a given teacher
    def get_teacher_c(self, teacher_name):
        return self.command("get_teacher_c", [teacher_name]).split("|")
    
    # gets a list of textbook titles
    def get_textbook_titles(self):
        return self.command("get_textbook_titles", []).split("|")