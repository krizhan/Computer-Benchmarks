#define _GNU_SOURCE

#include <sched.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
  
#include "tsc.h"
#include "common.h"

int main(int argc, char *argv[]){
    
    cpu_set_t  mask;
    CPU_ZERO(&mask);
    CPU_SET(0, &mask);
    int result = sched_setaffinity(0, sizeof(mask), &mask);
    if(result == -1){
        printf("Error running experiment, try again\n");
        return -1;
    }
    
    int num_processes = 2;
    int nperiods = 50;
    u_int64_t threshold = 1500;
    u_int64_t *samples = (u_int64_t *) malloc (2 * nperiods * sizeof(u_int64_t));
    
    double cpu_frequency = get_cpu_frequency();
    start_counter();
    
    u_int64_t start = get_counter();
    
    for(int i = 0; i < num_processes; i ++){
    
        int pid = fork();
        if(pid == 0){
            inactive_periods(nperiods, threshold, samples);
            print_duration(i, nperiods, start, samples, cpu_frequency);
            exit(0);
        }
        else if(pid == -1){
            printf("Error running experiment, try again\n");
            return -1;
        }
    }
    
    for (int i = 0; i < num_processes; i++) {
        int wstatus;
        pid_t pid = wait(&wstatus);
        if(pid == -1 || !WIFEXITED(wstatus)){
            printf("Error running experiment, try again\n");
            return -1;
        }
    }
    
    return 0;
}
