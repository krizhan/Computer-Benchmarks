#include <stdlib.h>

#include "tsc.h"
#include "common.h"

int main(int argc, char *argv[]){
   
    int nperiods = 30;
    
    u_int64_t *samples = (u_int64_t *) malloc (2 * nperiods * sizeof(u_int64_t));
    u_int64_t threshold = 1000;

    double cpu_frequency = get_cpu_frequency();
    
    start_counter();
    
    u_int64_t start = inactive_periods(nperiods, threshold, samples);
    print_duration(0, nperiods, start, samples, cpu_frequency);
    
    free(samples);
  
    return 0;
}
