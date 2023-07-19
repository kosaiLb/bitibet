import os
import json
from termcolor import colored

LIMIT = -2

tb_tennis_path = "./files/tennis/tb/"
fw_tennis_path = "./files/tennis/fw/"

def compare_date(tbDate, fwDate):
    for i in range(3):
        if not tbDate[i] == fwDate[i]:
            return False
    return True
  
def replace_str(n, words):
    for w in words:
        n = n.replace(w, " ")

    return n

def compare_eq_names(n1, n2):
    words = ['-', ',', '.', '\\', '/', 'fc', 'U21', 'w', 'women', 'FC', '(F)']
    if n1 in n2 or n2 in n1:
        return True
    n1 = replace_str(n1.strip(), words).split(' ')
    n2 = replace_str(n2.strip(), words).split(' ')
    count = 0
    for w1 in n1:
        for w2 in n2:
            if not w1 == ' ' and not w2 == ' ':
                if w1 == w2:
                    count += count
    if count > 0:
        return True
    return False

def F_Double(_type, x1, x2, tbeq1, tbeq2, fweq1, fweq2, Tbt_name, Fwt_name, date):
    total = 100 - (100/x1 + 100/x2)
    if total > LIMIT:
        print(f"""
{colored("==> "+str(total), 'green')}
            {tbeq1}, {tbeq2}
            {fweq1}, {fweq2}

            {_type}
            {x1} {x2}

            tour : {Tbt_name}, 
            tour : {Fwt_name}
            {colored(date, 'red')}
        """)

def calc_12(tb_1, tb_2, fw_1, fw_2, tbeq1, tbeq2, fweq1, fweq2, Tbt_name, Fwt_name, date):
    tb_1 = float(".".join(tb_1.split(',')))
    tb_2 = float(".".join(tb_2.split(',')))

    F_Double("tb_1, fw_2", tb_1, fw_2, tbeq1, tbeq2, fweq1, fweq2, Tbt_name, Fwt_name, date)
    F_Double("tb_2, fw_1", tb_2, fw_1, tbeq1, tbeq2, fweq1, fweq2, Tbt_name, Fwt_name, date)

def ok(Tbt_name, fw_tour_name):
    double = False
    _in = "Doubles" in Tbt_name and "Doubles" in fw_tour_name
    _not_in = "Doubles" not in Tbt_name and "Doubles" not in fw_tour_name
    if _in or _not_in:
        double = True
        # print(Tbt_name + " - " + fw_tour_name)
        # print(str(_in) + " - " + str(_not_in))
    return double

def calculate(Tbt_name, Fwt_name, Tbt, Fwt):
    for date in Tbt:
        tb_date = list(reversed(date.split('/')))
        for match_id in Tbt[date]:
            tb_match = Tbt[date][match_id]

            for fw_tour_name, fw_tour in Fwt.items():
                if ok(Tbt_name, fw_tour_name):
                    for match_id, fw_match in fw_tour.items():
                        fw_date = fw_match['date'].split('-')
                        if compare_date(tb_date, fw_date):
                            eq1 = compare_eq_names(tb_match["comp1"], fw_match["comp1"])
                            eq2 = compare_eq_names(tb_match["comp2"], tb_match["comp2"])

                            if eq1 and eq2:
                                if "1X2" in fw_match and "12" in tb_match["odds"]:
                                    tb_1 = tb_match["odds"]["12"]["1"]
                                    tb_2 = tb_match["odds"]["12"]["2"]
                                    fw_1 = fw_match["1X2"]["1"]
                                    fw_2 = fw_match["1X2"]["2"]

                                    calc_12(
                                        tb_1, tb_2,
                                        fw_1, fw_2,
                                        tb_match["comp1"],
                                        tb_match["comp2"],
                                        fw_match["comp1"],
                                        fw_match["comp2"],
                                        Tbt_name, fw_tour_name, date
                                    )

def compare():
    fw_names = os.listdir(fw_tennis_path)
    tb_file = open("./tb_tennis.json")
    tb_tours = json.load(tb_file)

    for fw_name in fw_names:
        fw_file = open(f"{fw_tennis_path}{fw_name}")
        fw_obj = json.load(fw_file)
        fw_name_flat = (fw_name.replace(".json", "")).lower()

        for tb_tour, tb_tour_obj in tb_tours.items():
            tb_tour_flat = tb_tour.lower()
            if fw_name_flat in tb_tour_flat:
                calculate(tb_tour, fw_name, tb_tour_obj, fw_obj)
            if fw_name_flat == "monde":
                if "wimbledon" in tb_tour_flat:
                    calculate(tb_tour, fw_name, tb_tour_obj, fw_obj)
                
        
def add_files():
    content = {}
    tb_files = os.listdir(tb_tennis_path)
    for tb_file in tb_files:
        file = open(f"{tb_tennis_path}{tb_file}")
        read_json_obj = json.load(file)
        for x, y in read_json_obj.items():
            content[x] = y
        file.close()

    tb_file_sum = open("./tb_tennis.json", "w")
    tb_json_obj = json.dumps(content, indent=4)
    tb_file_sum.write(tb_json_obj)
    tb_file_sum.close()
    
add_files()
compare()
