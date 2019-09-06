import requests
from bs4 import BeautifulSoup
import networkx as nx
import numpy as np

def get_change_val_pair(candidate_item):
    return int(candidate_item.next_sibling.next_sibling.text), int(candidate_item.next_sibling.next_sibling.next_sibling.next_sibling.text)

def scrape_one_result(i):
    page = requests.get('https://www.cambridgema.gov/election2017/Council%20Order%20Round' + str(i) + '.htm')
    soup = BeautifulSoup(page.content)
    candidates = [x for x in soup('table')[1]('th') if not x.text.isupper()]
    return [get_change_val_pair(x) for x in candidates]

def get_all_results():
    return [scrape_one_result(i) for i in range(1, 20)]

def get_candidate_names():
    page = requests.get('https://www.cambridgema.gov/election2017/Council%20Order%20Round' + str(2) + '.htm')
    soup = BeautifulSoup(page.content)
    return [x.text for x in soup('table')[1]('th') if not x.text.isupper()]

# get where vote is currently allocated
def get_current_assignment(ballot_arr):
    return np.take_along_axis(ballot_arr, (ballot_arr >= 0).argmax(axis=1), axis=0)

# array will be an N x C array, where N is the number of voters and C is the number of candidates.
# this assigns their #1 vote first
def initialize_ballot_array(results, names):
    init_allocation = [x[0] for x in results[0]]
    arr = np.array([[-1] * len(names)] * sum(init_allocation))
    arr[:,0] = np.concatenate([[i] * init_allocation[i] for i in range(len(init_allocation))])
    return arr

results = get_all_results()
names = get_candidate_names()
ballot_arr = initialize_ballot_array(results, names)
np.take_along_axis((ballot_arr >= 0).argmax(axis=1), ballot_arr, axis=0)
get_current_assignment(ballot_arr).shape


(ballot_arr >= 0).argmax(axis=1).shape
get_current_assignment(ballot_arr)
round
round = results[1]
[round[x] for x in range(len(round)) if round[x][0] < 0]
positive_indices = np.concatenate([[i] * abs(round[i][0]) for i in range(len(round)) if round[i][0] > 0])
positive_indices


def assign_next_round(ballot_arr, round):
    negative_indices = np.concatenate([[i] * abs(round[i][0]) for i in range(len(round)) if round[i][0] < 0])
    positive_indices = np.concatenate([[i] * abs(round[i][0]) for i in range(len(round)) if round[i][0] > 0])
    np.random.shuffle(negative_indices)
    np.random.shuffle(positive_indices)
    negative_indices = negative_indices[:len(positive_indices)]
    
    # there should always be more negative indices than positive ones. truncate
