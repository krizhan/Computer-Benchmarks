#define _GNU_SOURCE
#define _POSIX_C_SOURCE 199309L 

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "common.h"
#include "tsc.h"


double cycles_to_milliseconds(u_int64_t cycles, double cpu_frequency){
  return cycles / (cpu_frequency*10e2) ;
}

void insertionSort(double * samples, int size) { 
    double key;
    for (int i = 1; i < size; i++){ 
        key = samples[i]; 
        int j = i-1; 
  
        while (j >= 0 && samples[j] > key){ 
            samples[j+1] = samples[j]; 
            j = j-1; 
        } 
        samples[j+1] = key; 
   } 
} 

double binary_search_index(double *samples, double search_value, int start, int end, int max){
    if(start == end){
        return (max == 1) ? end : start;
    }
    else if(start > end){ //Doubt this case is necessary
        return (max == 1) ? end : start;
    }
    else{
        int middle = (start + end % 2 == 0) ? ((start + end) / 2): ((start + end + 1) / 2);
        if(search_value < samples[middle]){
            return binary_search_index(samples, search_value, start, middle - 1, max);
        }
        else if(search_value > samples[middle]){
            return binary_search_index(samples, search_value, middle + 1, end, max);
        }
        else{
            return middle;
        }
    }
    return 0;
}

double k_best_measurement(double * samples, int size){
    double tolerance_range = 0.01;
        
    double best_cluster = -1;
    int best_index = -1;
    for(int i = 0; i < size; i ++){
            
        double min_tolerance = samples[i] - tolerance_range * samples[i];
        double max_tolerance = samples[i] + tolerance_range * samples[i];
        int cluster_size = binary_search_index(samples, max_tolerance, 0, size, 1) - binary_search_index(samples, min_tolerance, 0, size, 0); 
        if(cluster_size > best_cluster){
            best_index = i;
            best_cluster = cluster_size;
        }
    }
    return samples[best_index];
}

double get_cpu_frequency(){
    
    int total_clock_samples = 10;
    double *clock_samples = (double *) malloc( total_clock_samples * sizeof(double));
    
    for(int i = 1; i < total_clock_samples; i ++){

        struct timespec ts;
        int milliseconds = 500 * i;
        ts.tv_sec = milliseconds / 1000;
        ts.tv_nsec = (milliseconds % 1000) * 1000000;

        start_counter();
        nanosleep(&ts, NULL);
        clock_samples[i] = get_counter() / (milliseconds * 1e3);;
    }
    
    insertionSort(clock_samples, total_clock_samples);

    return k_best_measurement(clock_samples, total_clock_samples);
}


u_int64_t inactive_periods(int num, u_int64_t threshold, u_int64_t * samples){
	int records = 0;
	u_int64_t current, last, start;
    
	last = current = start = get_counter();
	while (records != num) {
                last = current;
		current = get_counter();
		if (current - last > threshold) {
			samples[2 * records] = last;
			samples[2 * records + 1] = current;
			records++;
		}
		
	}
	return start;
}

void print_duration(int process, int nperiods, u_int64_t start, u_int64_t * samples, double cpu_frequency){
    
    u_int64_t previous = start;
    for (int k = 0; k < 2 * nperiods; k = k + 2) {
        
        fprintf(stdout, "(Process %d) Active %d: start at %ld (%f ms), duration %ld cycles (%f ms)\n", process,
                k / 2, previous, cycles_to_milliseconds(previous, cpu_frequency), samples[k] - previous, cycles_to_milliseconds(samples[k] - previous, cpu_frequency));
        previous = samples[k];
        
        fprintf(stdout, "(Process %d) Inactive %d: start at %ld (%f ms), duration %ld cycles (%f ms)\n", process,
                k / 2, previous, cycles_to_milliseconds(previous, cpu_frequency), samples[k + 1] - previous, cycles_to_milliseconds(samples[k + 1] - previous, cpu_frequency));
        previous = samples[k + 1];
    }
}
