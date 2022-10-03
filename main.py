# Implement the following algorithms
# First-Come
# First-Served (FCFS)
# Shortest-Job First (SJF)
# Round Robin (RR)

# The program takes inputs
#   - File name contains: which process arrives when, how much CPU time it requests, Burst Time
#   - The name of the algorithm
#   - If RR --> the Time quantum in milliseconds

# PID   Waiting Time    Turnaorund Time

# The program computes
#   - The waiting time, and turnaround time, for the respective process
#   - The average waiting time, and average turnaround time

import sys
import os

import argparse
import sys

is_windows = sys.platform.startswith('win')
# Console Colors
if is_windows:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'  # white
    try:
        import win_unicode_console, colorama
        win_unicode_console.enable()
        colorama.init()
    except:
        print(
            "[!] Error: Coloring libraries not installed, no coloring will be used"
        )
        G = Y = B = R = W = G = Y = B = R = W = ''

else:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'  # white


def parser_error(errorMessage):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    print(R + "Error: " + errorMessage + W)
    sys.exit()


#sched -f <process information file> -a [FCFS | SJF | RR] [-q <time quantum>]
def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' +
                                     sys.argv[0] + "-f file.txt -a SJF")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-f',
                        '--file',
                        help="File name to retrieve the data from",
                        required=True)
    parser.add_argument('-a',
                        '--algorithm',
                        help="The algorithm to be used to calculate the data",
                        required=True)
    parser.add_argument('-q',
                        '--quantom-time',
                        help="The quantom time of the RR algorithm",
                        type=int,
                       default = 2)
    return parser.parse_args()


def array_copy(arr):
  newArr = []
  for i in arr:
    newArr.append(i)
  return newArr

def average(array):
  """Returns the average of the given array"""
  avr = 0
  for i in array:
    avr += i
  avr /= len(array)
  return avr

# Search function to search in a List
def searchInList(list, algo):
    for i in range(len(list)):
        if list[i] == algo:
            return True
    return False

def sort_by(main_arr, sub_arrays, fromIndex, toIndex):
  """This function sorts the main_arr and sub_arrays based on main_arr from lowest to highest, if there is equal values sorting become based on sub_arrays first array then second then third etc """
  #if toIndex == 0:
  #  toIndex = len(main_arr)
  # sort by main
  # generate unclear array 
  # ------------------ sorting ------------------------
  main_index_arr = range( fromIndex , toIndex +1)
  for j in main_index_arr:
    for i in main_index_arr:
      if main_arr[j] < main_arr[i]:
        temp = main_arr[i]
        main_arr[i] = main_arr[j]
        main_arr[j] = temp

        # sorting sub arrays
        if len(sub_arrays) == 0: return 0
        for arr in sub_arrays:
          temp = arr[i]
          arr[i] = arr[j]
          arr[j] = temp
    ### for i end
  ### for j end

  # ---------------------------------------------------
  # ---------- generating unclear_arr -----------------
  # to be compared with next number in the array if equal then unclear_count++
  unclear_num = 0   
  unclear_count = 0
  unclear_arr = []
  # fromIndex + 1 cuz we compare between 'i' and 'i - 1' 
  for i in range(fromIndex + 1, toIndex + 1 ):
    unclear_num = main_arr[i - 1]
    if main_arr[i] == unclear_num:
        unclear_count += 1
    else:
      if unclear_count > 0:
        # append the range to the unclear_arr
        unclear_arr.append([i - unclear_count - 1, i - 1])
        unclear_count = 0
    if i == toIndex and unclear_count > 0:
      unclear_arr.append([i - unclear_count, i])
  ### for i end
  # ---------------------------------------------------
  # ------------------ recursion ----------------------
  # next sub array will include all elements in sub_arrays but not first
  next_sub_arrays = [] 
  for i in range(1, len(sub_arrays) ):
    next_sub_arrays.append(sub_arrays[i])

  for index_arr in unclear_arr:
    sort_by(sub_arrays[0], next_sub_arrays, index_arr[0], index_arr[1])
  
  ### sort_by end
  

def readFile(FileName):
    """ The Function does not check for security inputs, file format should be
        <int>,<int>,<int>\n
    """
    PID = []
    arrival = []
    burst = []
    with open(FileName) as input_data:
        for line in input_data:
            n, a, b = line.split(',')
            PID.append(int(n))
            arrival.append(int(a))
            burst.append(int(b))
    return (PID, arrival, burst)


def main(file, algo, time):

    #Check if file exist
    if len(file) > 0:
        if os.path.exists(file):
            # pid, arrival, burst: is lists from the file
            # lines_coutner: counts the lines in the file for a for-loop
            pid, arrival, burst = readFile(file)
        else:
            print("File \"%s\" does no exist\n" % file)
    else:
        print("Missing argument/file\n")
    #Check if algo submitted
    ListAlgo = ['FCFS', "SJF", "RR"]
    waiting_time = []
    turnaround_time = []
    if len(algo) > 0:
        if searchInList(ListAlgo, algo):
            if (algo == "FCFS"):
                pid, waiting_time, turnaround_time = FCFS(pid, arrival, burst)
                #print(waiting_time)
            elif (algo == "SJF"):
                pid, waiting_time, turnaround_time = SJF(pid, arrival, burst)
            elif (algo == "RR"):
                pid, waiting_time, turnaround_time = RR(
                    pid, arrival, burst, time)

        else:
            print("The algorithm is not supported")
            sys.exit()
    else:
        print("Missing argument/file\n")
        sys.exit()

    # print all data
    #print(len(pid))
    #print(len(waiting_time))
    print_table(pid, waiting_time, turnaround_time, file, algo)


def FCFS(pid, arrival, burst):
    waiting_time = []
    turnaround_time = []
    pid_arr = array_copy(pid)
    arrival_arr = array_copy(arrival)
    burst_arr = array_copy(burst)
    processor_time = 0
    new_pid = []
    for i in range(len(pid)):

        # index for element with min arrival time
        # Retriev the First Process Index, that have the smallest Arriaval Time
        min_t_index = arrival_arr.index(min(arrival_arr))

        #processor_time += burst_arr[ min_t_index ]
        if processor_time >= arrival_arr[min_t_index]:
            waiting_time.append(processor_time - arrival_arr[min_t_index])
            processor_time += burst_arr[min_t_index]
        else:
            waiting_time.append(0)
            processor_time = arrival_arr[min_t_index] + burst_arr[min_t_index]

        #print(processor_time)
        turnaround_time.append(processor_time - arrival_arr[min_t_index])
        #
        arrival_arr.pop(min_t_index)
        new_pid.append(pid_arr[min_t_index])
        pid_arr.pop(min_t_index)
        burst_arr.pop(min_t_index)
    # loop
    # check pid
    # run this process (time)
    # Waitin_time is a [list]
    # print("waiting time:", waiting_time)
    # print("turnaround time:", turnaround_time)

    print(average(waiting_time))

    print(average(turnaround_time))

    return (new_pid, waiting_time, turnaround_time)


def SJF(pid, arrival, burst):
    """Shortest Job First
      1- Check the arrival time
      2- Run until the next arrival time, and check if Burst time larger or smaller
      3- If no one arrives run the process until it ends
    """
    waiting_time = []
    turnaround_time = []
    pid_arr = array_copy(pid)
    arrival_arr = array_copy(arrival)
    burst_arr = array_copy(burst)
    processor_time = 0
    ready_burst_arr = []
    ready_pid_arr = []
    ready_arrival_arr = []
    new_pid = []
    sort_by(arrival_arr, [burst_arr, pid_arr], 0, len(arrival_arr) - 1)
    
    j = 0
    for i in range(len(pid)):  # process all arrays
        while j < len(pid) and arrival_arr[j] <= processor_time:  # arrival <= process_time
            ready_burst_arr.append(burst_arr[j])
            ready_pid_arr.append(pid_arr[j])
            ready_arrival_arr.append(arrival_arr[j])
            j += 1

        if j < len(pid) and len(ready_burst_arr) == 0:
            ready_burst_arr.append(burst_arr[j])
            ready_pid_arr.append(pid_arr[j])
            ready_arrival_arr.append(arrival_arr[j])
            processor_time = arrival_arr[j]
            j += 1

        min_i = ready_burst_arr.index(min(ready_burst_arr))

        processor_time += ready_burst_arr[min_i]

        turnaround_time.append(processor_time - ready_arrival_arr[min_i])
        waiting_time.append(turnaround_time[i] - ready_burst_arr[min_i])
        new_pid.append(ready_pid_arr[min_i])

        ready_burst_arr.pop(min_i)
        ready_arrival_arr.pop(min_i)
        ready_pid_arr.pop(min_i)

    return (new_pid, waiting_time, turnaround_time)


def RR(pid, arrival, burst, time):
    """
    
    
    
    The Round Robin is done
    
    
    
    
    
    """
    pid_arr = array_copy(pid)
    arrival_arr = array_copy(arrival)
    burst_arr = array_copy(burst)
    
    waiting_time = []
    turnaround_time = []
    new_pid = []
    process_time = 0
    individual_waiting = [0] * len(pid)
    
    
    sort_by(arrival_arr, [burst_arr, pid_arr], 0, len(arrival_arr) - 1)
    remaining_burst = array_copy(burst_arr)
    total_time_remaining = sum(burst_arr)
    
    # print(pid_arr)
    # print(arrival_arr)
    # print(burst_arr)
    
    while total_time_remaining != 0:
        for i in range(len(pid)):
            if remaining_burst[i] <= time and remaining_burst[i] >= 0 and arrival_arr[i] <= process_time:
                process_time += remaining_burst[i]
                total_time_remaining -= remaining_burst[i]
                remaining_burst[i] = 0
            elif remaining_burst[i] > 0 and arrival_arr[i] <= process_time:
                remaining_burst[i] -= time
                total_time_remaining -= time
                process_time += time
            elif arrival_arr[i] > process_time:
                process_time = arrival_arr[i]


            if remaining_burst[i] == 0 and individual_waiting[i] != 1:
                waiting_time.append(process_time - arrival_arr[i] - burst_arr[i])
                turnaround_time.append(process_time - arrival_arr[i])
                new_pid.append(pid_arr[i])

                
                individual_waiting[i] = 1

    # print("waiting time:", waiting_time)
    # print("turnaround time:", turnaround_time)

    return (new_pid, waiting_time, turnaround_time)




def print_table(pid, waiting_time, turnaround_time, file, algo):
    print("-------------------------------------------------------------\n")
    print("Process information from file: " + file +
          "\nScheduling algorithm: " + algo + "\n\n")
    print('PID\t\t\t\t\tWaiting Time (ms)\t\tTurnaround Time (ms)\n')
    for i in range(len(pid)):
        if waiting_time:
            #print(waiting_time)
            #print(i, len(pid), pid[i], waiting_time[i])
            print(
                str(pid[i]) + '\t\t\t\t' + str(waiting_time[i]) +
                '\t\t\t\t\t\t' + str(turnaround_time[i]))

    print("\n\nAverage waiting time: " + str(average(waiting_time)) +
          " ms\nAverage turnaround time:  " + str(average(turnaround_time)))

    print("-------------------------------------------------------------\n")


def interactive():
    args = parse_args()
    file = args.file
    algo = args.algorithm.upper()
    time = args.quantom_time
    main(file, algo, time)


if __name__ == "__main__":
    interactive()
