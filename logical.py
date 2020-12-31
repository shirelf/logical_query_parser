import switch as switch
from Tools.scripts.treesync import raw_input
#SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE Customers.Name=Orders.CustomerName AND Orders.Price>1000




class Algebrian_struct:
    def __init__(self, sub_select, sub_where, sub_from, str=None):
        self.p = sub_select
        self.s = []
        self.s.append(sub_where)
        self.c = sub_from
        self.str = str
        self.sigma_after_rule_four = []

    def trans_to_str(self):
        if len(self.s) == 1:
            self.str = "PI[" + str(self.p) + "](SIGMA[" + str(self.s[0]) + "](CARTESIAN(" + str(self.c) + ")))"
            self.str=self.str.replace(" ","")
        else:
            self.str = "PI[" + str(self.p) + "](SIGMA[" + str(self.s[0]) + "](SIGMA[" + str(self.s[1]) + "](CARTESIAN(" + str(self.c) + ")))"
            self.str = self.str.replace(" ", "")
        print(self.str)

    def execute_rule_four(self):
        and_loc = self.s[0].find('AND')
        if and_loc != -1:
            sigma_one = self.s[0][0:and_loc]
            sigma_second = self.s[0][and_loc + 4:]
            self.s.clear()
            self.s.append(sigma_one)
            self.s.append(sigma_second)
            self.trans_to_str()
    def swap_sigmas(self):
        temp = self.s[0]
        self.s[0] = self.s[1]
        self.s[1] = temp
        self.trans_to_str()

def receive_input():
    query = input()
    if query.endswith(";"):
        query = query[:-1]
    select_first = query.find("SELECT")
    select_last = query.find("FROM")
    sub_select = query[select_first: select_last]
    sub_select = sub_select[7:]

    from_first = query.find("FROM")
    from_last = query.find("WHERE")
    sub_from = query[from_first:from_last]
    sub_from = sub_from[5:]

    where_first = query.find("WHERE")
    sub_where = query[where_first:]
    sub_where = sub_where[6:]
    new_query = Algebrian_struct(sub_select, sub_where, sub_from)


    return new_query


# def build_algebrian_expression():


def execute_rule_b(new_query):
    new_query.swap_sigmas()

def execute_rule(new_query, rule):
    if rule is 'a':
        execute_rule_a(new_query)
        print(new_query.str) # after activite rule 4
    if rule is 'b':
        execute_rule_b(new_query)
        print(new_query.str)  # after activite rule 4a
    if rule is 'c':
        execute_rule_b(new_query)
        print(new_query.str)  # after activite rule 4a


def execute_rule_a(new_query):
    new_query.execute_rule_four()




def main_program():
    new_query = receive_input()
    Algebrian_struct.trans_to_str(new_query)
    print(new_query.str)
    print("please choose one of the rules:\na. 4 \nb. 4a \nc. 6,6a\nd. 5a\ne. 11b\n")
    rule= input()
    execute_rule(new_query,rule)


main_program()