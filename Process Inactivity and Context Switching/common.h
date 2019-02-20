u_int64_t inactive_periods(int num, u_int64_t threshold, u_int64_t * samples);

void print_duration(int process, int nperiods, u_int64_t start, u_int64_t * samples, double cpu_frequency);

double get_cpu_frequency();