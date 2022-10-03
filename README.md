# CPU-Scheduling
The program calculates the waiting time and the burst time with the Shortest-Job-First (SJF), First-Come-First-Served (FCFS) and Round-Robin (RR) algorithms.

## Usage
```
usage: main.py [-h] -f FILE -a ALGORITHM [-q QUANTOM_TIME]

OPTIONS:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File name to retrieve the data from
  -a ALGORITHM, --algorithm ALGORITHM
                        The algorithm to be used to calculate the data
  -q QUANTOM_TIME, --quantom-time QUANTOM_TIME
                        The quantom time of the RR algorithm

Example: python .\main.py-f file.txt -a SJF
```
