"""
This is my implementation of project 1 for Artificial intelligence. It is essentially just a basic program with a
that reads in from a file and performs a few basic algorithms.

James Smith
Project 1
n01400606@osprey.unf.edu
"""

import csv
import re

class State:
    """This class holds the information about a US State"""

    # Constructor

    def __init__(self, state, capital, abbr, pop, region, reps):
        self.state = state
        self.capital = capital
        self.abbr = abbr
        self.pop = pop
        self.region = region
        self.reps = reps

    # Getters

    def get_state(self):
        return self.state

    def get_capital(self):
        return self.capital

    def get_abbr(self):
        return self.abbr

    def get_pop(self):
        return self.pop

    def get_region(self):
        return self.region

    def get_reps(self):
        return self.reps

    # Setters

    def set_state(self, state):
        self.state = state

    def set_capital(self, capital):
        self.capital = capital

    def set_abbr(self, abbr):
        self.abbr = abbr

    def set_pop(self, pop):
        self.pop = pop

    def set_region(self, region):
        self.region = region

    def set_reps(self, reps):
        self.reps = reps

    # Greater than

    def __gt__(self, state_a, state_b):
        return state_a > state_b

    # To string

    def __str__(self):
        return '\n' + "State Name: " + self.state + '\n' + "Capital City: " + self.capital + '\n' + "State Abbr: " + \
               self.abbr + '\n' + "State Population: " + str(self.pop) + '\n' "Region: " + self.region + '\n' + \
               "US House Seats: " + str(self.reps) + '\n'



def menu():
    """Menu prompt"""
    print("1) Print a state report")
    print("2) Sort by state name")
    print("3) Sort by population")
    print("4) Find and print a given state")
    print("5) Quit")
    ans = raw_input("Enter your choice: ")
    return ans


def state_report(states_info):
    """State report for user input 1"""
    dash = '-' * 120
    for i in range(len(states_info)):
        if i == 0:
            print dash
            print('{:<15s}{:>16s}{:>22s}{:>15s}{:>17s}{:>25s}'.format(states_info[i].get_state(),
                                                                      states_info[i].get_capital(),
                                                                      states_info[i].get_abbr(),
                                                                      states_info[i].get_pop(),
                                                                      states_info[i].get_region(),
                                                                      states_info[i].get_reps()))
            print dash
        else:
            print('{:<20s}{:^15s}{:^23s}{:^11s}{:^28s}{:>8s}'.format(states_info[i].get_state(),
                                                                     states_info[i].get_capital(),
                                                                     states_info[i].get_abbr(),
                                                                     states_info[i].get_pop(),
                                                                     states_info[i].get_region(),
                                                                     states_info[i].get_reps()))
    print dash


def quicksort_names(arr, low, hi):
    """Generic quicksort recursive algorithm used for user input 2"""
    if low < hi:
        part = partition(arr, low, hi)
        quicksort_names(arr, low, part - 1)
        quicksort_names(arr, part + 1, hi)


def partition(arr, low, hi):
    """Generic partitioning algorithm for recursive quicksort"""
    pivot = arr[hi].get_state()
    j = low - 1
    for i in range(low, hi):
        if arr[i].get_state() < pivot:
            j += 1
            arr[j], arr[i] = arr[i], arr[j]
    arr[j + 1], arr[hi] = arr[hi], arr[j + 1]
    return j + 1


def sort_pop(arr):
    """Generic sort"""
    i = 1
    while i < len(arr):
        j = 1
        while j < len(arr):
            if int(arr[i].get_pop()) < int(arr[j].get_pop()):
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
            j += 1
        i += 1

def binary_search(state_list, target):
    """Generic binary search algorithm for user input 4"""
    hi = len(state_list)
    low = 0

    while(low <= hi):
        mid = (hi + low) / 2
        if state_list[mid].get_state() == target:
            print state_list[mid]
            return
        elif target < state_list[mid].get_state():
            hi = mid - 1
        else:
            low = mid + 1

    print"\nNot found\n"


def sequential_search(state_list, target):
    """Generic sequential search algorithm for user input 4"""
    for state in state_list:
        if state.get_state() == target:
            print state
            return

    print "\nNot found\n"


# a list to store the information about the states
states_info = []

# read in the file
with open('States.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        x = State(row[0], row[1], row[2], row[3], row[4], row[5])
        states_info.append(x)

# boolean to call either binary search or sequential search
sorted = False
# call the menu
ans = menu()
# continue the loop
cont = True

while cont:
    if ans == '1':
        state_report(states_info)
        ans = menu()
        continue
    elif ans == '2':
        quicksort_names(states_info, 1, len(states_info) - 1)
        print "\nStates sorted by names\n"
        sorted = True
        ans = menu()
        continue
    elif ans == '3':
        sort_pop(states_info)
        print "\nStates sorted by population\n"
        sorted = False
        ans = menu()
        continue
    elif ans == '4':
        answer = raw_input("Enter the State name: ")
        if sorted:
            binary_search(states_info, answer)
        else:
            sequential_search(states_info, answer)
        ans = menu()
        continue
    elif ans == '5':
        cont = False
    else:
        while not re.match("[1-5]", ans):
            ans = raw_input("Invalid choice please enter 1-5: ")
