import reframe as rfm
import reframe.utility.sanity as sn

class OSUBenchmarkBase(rfm.RegressionTest):
    valid_systems = ['aion:batch', 'iris:batch']
    valid_prog_environs = ['foss', 'system-gcc']
    num_tasks = 2
    num_tasks_per_node = 2
    num_cpus_per_task = 1
    executable = 'osu_latency'  # Default, overridden in derived classes
    tags = {'performance', 'mpi', 'numa'}

    @run_before('run')
    def set_numa_options(self):
        system = self.current_system.name
        if system == 'aion':
            # Aion: 8 NUMA nodes (4 per socket), bind to cores 0 and 1 (same socket)
            self.job.options = ['--ntasks-per-socket=1', '--cpu-bind=map_cpu:0,1']
        elif system == 'iris':
            # Iris: 2 NUMA nodes per socket, bind to cores 0 and 14 (different NUMA)
            self.job.options = ['--ntasks-per-socket=1', '--cpu-bind=map_cpu:0,14']

    @sanity_function
    def validate_results(self):
        return sn.assert_found(r'^8192\s+\d+\.\d+', self.stdout)

@rfm.simple_test
class OSULatencyTest(OSUBenchmarkBase):
    def __init__(self):
        super().__init__()
        self.executable = 'osu_latency'
        self.executable_opts = ['-m', '8192']
        self.reference = {
            'aion:batch': {
                'latency': (2.3, None, 0.1, 'µs'),  # Expected ~2.3 µs ±10%
            },
            'iris:batch': {
                'latency': (1.8, None, 0.1, 'µs'),  # Adjust based on Iris specs
            }
        }

    @run_before('performance')
    def extract_latency(self):
        self.perf_variables = {
            'latency': sn.extractsingle(r'^8192\s+(\d+\.\d+)', self.stdout, 1, float)
        }

@rfm.simple_test
class OSUBandwidthTest(OSUBenchmarkBase):
    def __init__(self):
        super().__init__()
        self.executable = 'osu_bw'
        self.executable_opts = ['-m', '1048576']
        self.reference = {
            'aion:batch': {
                'bandwidth': (12000, None, 0.1, 'MB/s'),  # Expected ~12,000 MB/s ±10%
            },
            'iris:batch': {
                'bandwidth': (10000, None, 0.1, 'MB/s'),  # Adjust for Iris
            }
        }

    @run_before('performance')
    def extract_bandwidth(self):
        self.perf_variables = {
            'bandwidth': sn.extractsingle(r'^1048576\s+(\d+\.\d+)', self.stdout, 1, float)
        }
