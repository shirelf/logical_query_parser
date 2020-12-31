
tables = ["Customers", "Orders"]
operators = ["<", ">", "="]


#select parser


def is_distinct(distinctString):
    if distinctString.find("DISTINCT", 0, 9) != -1:
        distinctString = distinctString[8:]
    is_attribute_list(distinctString);


def is_attribute_list(attributeListString):
    if attributeListString == '*':
        return True
    else:
        is_att_list(attributeListString)


def is_att_list(attListString):
    flag = False
    select_first = attListString.find(",")
    if select_first == -1:
        flag = is_attribute(attListString)
        if not flag:
            exit("Parsing <attribute_list> failed")
    else:
        is_att_list(attListString[select_first + 1:])
        flag = is_attribute(attListString[:select_first])
        if not flag:
            exit("Parsing <attribute_list> failed")

# From parser


def is_table_list(tableListString):
    flag = False
    from_first = tableListString.find(",")
    if from_first == -1:
        flag = is_table(tableListString)
        if not flag:
            exit("Parsing <table_list> failed")
    else:
        is_table_list(tableListString[from_first + 1:])
        flag = is_table(tableListString[:from_first])
        if not flag:
            exit("Parsing <table_list> failed")


def is_table(tableStr):
    flag = False
    listOfTables = ['Customers', 'Orders']
    for i in range(2):
        if tableStr == listOfTables[i]:
            flag = True
    return flag


#condtion parser


def is_condition(condition_str):
    valid_flag = False
    condition_str = condition_str.replace(" ", "")
    if condition_str.startswith("(") and condition_str.endswith(")"):
        valid_flag = is_condition(condition_str[1:-1])
        if valid_flag:
            return valid_flag
    if "AND" in condition_str:
        for i in condition_str:
            j = condition_str.find("AND")
            if j != -1:
                left = condition_str[0:j]
                right = condition_str[j + 3:]
                valid_flag = is_condition(left) and is_condition(right)
                if valid_flag:
                    return valid_flag
    if "OR" in condition_str:
        for i in condition_str:
            j = condition_str.find("OR")
            if j != -1:
                left = condition_str[:j]
                right = condition_str[j + 2:]
                left_flag = is_condition(left)
                right_flag = is_condition(right)
                valid_flag = left_flag and right_flag
                if valid_flag:
                    return valid_flag
    return is_simple_condition(condition_str)


def is_simple_condition(simpleConditionStr):
    sub_condition = simpleConditionStr.replace(" ", "")
    for i in range(len(sub_condition)):
        if sub_condition[i] in operators:
            valid_op_len = 1
            if sub_condition[i + 1] in operators:
                if sub_condition[i] == '=':
                    exit("Parsing <condition> failed")
                if sub_condition[i + 1] == '<':
                    exit("Parsing <condition> failed")
                valid_op_len = 2
            sub_left_condition = sub_condition[:i]
            sub_right_condition = sub_condition[i + valid_op_len:]
            sub_left_flag = False
            sub_right_flag = False
            sub_left_flag = is_constant(sub_left_condition)
            sub_right_flag = is_constant(sub_right_condition)
            if not sub_left_flag or not sub_right_flag:
                return exit("Parsing <condition> failed")
            if not is_compare_correct(sub_left_condition, sub_right_condition):
                return exit("Parsing <condition> failed")
            return True


def is_compare_correct(sub_left_condition, sub_right_condition):
    flag = False
    if sub_left_condition == "Customers.Name" or "Orders.CustomerName" or "Orders.Product":
        if is_str(sub_right_condition):
            flag = True
    if sub_left_condition == "Customers.Age" or "Orders.Price":
        if is_signed_int(sub_right_condition):
            flag = True
    if sub_left_condition == "Customers.Name":
        if sub_right_condition == "Orders.CustomerName":
            flag = True
    if sub_left_condition == "Orders.CustomerName":
        if sub_right_condition == "Customers.Name":
            flag = True
    return flag


def is_constant(constantStr):
    flag = is_number(constantStr) or is_str(constantStr) or is_attribute(constantStr)
    return flag


def is_str(strCheck):
    flag = False
    if strCheck.startswith("'") and strCheck.startswith("'"):
        flag = True
    if strCheck.startswith('"') and strCheck.startswith('"'):
        flag = True
    strCheck = strCheck[1:-1]
    return strCheck.isalpha()


def is_number(numberStr):
    return is_signed_int(numberStr)


def is_signed_int(unsignedIntStr):
    flag = True
    if not unsignedIntStr[0].isdigit():
        return False
    elif len(unsignedIntStr) == 1:
        if not unsignedIntStr[0].isdigit():
            return False
    else:
        flag = is_signed_int(unsignedIntStr[1:])
    return flag


def is_attribute(attributeStr):
    flag = False
    listOfAttributes = ['Customers.Name', 'Customers.Age', 'Orders.CustomerName', 'Orders.Product', 'Orders.Price']
    for i in range(5):
        if attributeStr == listOfAttributes[i]:
            flag = True
    return flag


# main program
query = input()
if query.endswith(";"):
    query = query[:-1]
select_first = query.find("SELECT")
select_last = query.find("FROM")
sub_select = query[select_first: select_last]
sub_select = " ".join(sub_select.split())
sub_select = sub_select[7:]
is_distinct(sub_select)

from_first = query.find("FROM")
from_last = query.find("WHERE")
sub_from = query[from_first:from_last]
sub_from = " ".join(sub_from.split())
sub_from = sub_from[5:]
is_table_list(sub_from)

where_first = query.find("WHERE")
sub_where = query[where_first:]
sub_where = " ".join(sub_where.split())
sub_where = sub_where[6:]
flag = is_condition(sub_where)
if not flag:
    exit("Parsing <condition> failed")