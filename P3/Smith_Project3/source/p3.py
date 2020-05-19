import os
import tempfile
from subprocess import PIPE, Popen
from tkinter import *

# Attributes, Hard Constraints, Preferences
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText


def get_input():
    attributes_input = attributes.get(1.0, END).lower()
    constraints_input = hard_constraints.get(1.0, END).lower()
    preferences_input = preferences.get(1.0, END).lower()
    success = parse_input(attributes_input, constraints_input, preferences_input)
    if not success:
        messagebox.showerror("Parse Error", "Cannot parse the input. Please use the correct format.")


def parse_input(attributes_input, constraints_input, preferences_input):
    att_re = re.compile("[a-z]+:?\s+[a-z]+,?\s+[a-z]+")
    att_list = attributes_input.split('\n')
    att_dict = {}
    att_counter = -1
    result.insert(END, "Converted Attributes:\n")
    for line in att_list:
        if line == '':
            continue
        elif att_re.search(line.strip()) is None:
            return False
        else:
            # getting rid of the ',' character in order to store
            temp_list = line.split()
            temp_string = temp_list[1]
            temp_string = temp_string[:-1]
            temp_list[1] = temp_string
            # associating the attributes with complementary values
            att_dict[temp_list[1]] = str(abs(att_counter))
            att_dict["not " + temp_list[2]] = str(abs(att_counter))
            att_dict["not " + temp_list[1]] = str(att_counter)
            att_dict[temp_list[2]] = str(att_counter)
            result.insert(END, str(abs(att_counter)) + ", " + str(att_counter) + "\n")
            att_counter -= 1
    con_list = constraints_input.split('\n')
    con_string = ''
    parsed_con = []
    result.insert(END, "Converted Constraints:\n")
    temp_clasp = ''
    for line in con_list:
        if line == '':
            continue
        else:
            temp_list = line.split()
            temp_string = ''
            for item in temp_list:
                if item == 'not':
                    temp_string += 'not '
                elif item == 'and':
                    con_string += '0'
                    parsed_con.append(con_string)
                    result.insert(END, con_string + "\n")
                    temp_clasp += con_string + "\n"
                    con_string = ''
                    temp_string = ''
                elif item == 'or':
                    continue
                else:
                    temp_string += item
                    con_string += att_dict.get(temp_string) + ' '
                    temp_string = ''
            con_string.strip()
            con_string += '0'
            parsed_con.append(con_string)
            result.insert(END, con_string + "\n")
            temp_clasp += con_string + "\n"
            con_string = ''
    pref_list = preferences_input.split('\n')
    pref_string = ''
    parsed_prefs = []
    pref_values = []
    result.insert(END, "Converted Preferences:\n")
    for line in pref_list:
        if line == '':
            continue
        else:
            temp_list = line.split()
            temp_value = temp_list.pop()
            pref_values.append(temp_value)
            temp_string = ''
            for item in temp_list:
                if ',' in item:
                    item = re.sub(',', '', item)
                if item == 'not':
                    temp_string += 'not '
                elif item == 'and':
                    pref_string += '0'
                    parsed_prefs.append(pref_string)
                    result.insert(END, pref_string + " Penalty Value = " + temp_value + "\n")
                    pref_string = ''
                    temp_string = ''
                elif item == 'or':
                    continue
                else:
                    temp_string += item
                    pref_string += att_dict.get(temp_string) + ' '
                    temp_string = ''
            pref_string.strip()
            pref_string += '0'
            parsed_prefs.append(pref_string)
            result.insert(END, pref_string + " Penalty Value = " + temp_value + "\n")
            pref_string = ''
    clasp_input = "p cnf " + str(abs(att_counter) - 1) + " " + str(len(parsed_con)) + "\n" + temp_clasp
    result.insert(END, "Clasp Input:\n" + clasp_input)
    run_clasp(clasp_input)
    return True


def run_clasp(clasp_input):
    text_file = open("clasp_input.txt", "w")
    text_file.write(clasp_input)
    text_file.close()
    process = Popen(["clasp", "0", "clasp_input.txt"], stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    result.insert(END, "Clasp Output:\n")
    result.insert(END, out)
    os.remove("clasp_input.txt")



def get_attributes_file():
    file = filedialog.askopenfilename()
    attributes.insert(END, open(file).read())


def get_hc_file():
    file = filedialog.askopenfilename()
    hard_constraints.insert(END, open(file).read())


def get_preferences_file():
    file = filedialog.askopenfilename()
    preferences.insert(END, open(file).read())


root = Tk()
root.title("Project 3: Clasp GUI")
Label(root, text="Attributes").grid(row=0, column=0)
attributes = ScrolledText(root, height=20, width=35)
attributes.grid(row=1, column=0)
Label(root, text="Hard Constraints").grid(row=0, column=0)
hard_constraints = ScrolledText(root, height=20, width=35)
hard_constraints.grid(row=1, column=1)
Label(root, text="Preferences").grid(row=0, column=0)
preferences = ScrolledText(root, height=20, width=35)
preferences.grid(row=1, column=2)
result = ScrolledText(root, height=20, width=35)
result.grid(row=1, column=4)
run = Button(root, text="RUN", command=get_input)
run.grid(row=0, column=4)
upload_attributes = Button(root, text="UPLOAD ATTRIBUTES", command=get_attributes_file)
upload_attributes.grid(row=0, column=0)
upload_hc = Button(root, text="UPLOAD CONSTRAINTS", command=get_hc_file)
upload_hc.grid(row=0, column=1)
upload_preferences = Button(root, text="UPLOAD PREFERENCES", command=get_preferences_file)
upload_preferences.grid(row=0, column=2)

attributes.insert(END, "drink: water, coffee\nalcohol: wine, beer\nsoda: coke, pepsi\nappetizer: soup, salad\n"
                       "breakfast: eggs, toast\nlunch: sandwich, burger\ndinner: fish, beef\ndessert: cake, icecream")
hard_constraints.insert(END, "soup OR NOT beer\nsoup OR NOT wine\nsandwich OR NOT cake\nwater AND NOT fish\n"
                             "soup OR NOT eggs OR NOT sandwich\neggs OR pepsi ")
preferences.insert(END, "fish AND wine, 7\ncoke OR eggs, 6\ncake OR burger, 5\neggs AND icecream, 3\nwater OR soup, 10"
                        "\nbeer AND burger, 9\ntoast OR pepsi, 8")

mainloop()
