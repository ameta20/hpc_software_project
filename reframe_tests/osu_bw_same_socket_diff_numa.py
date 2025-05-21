import reframe as rfm
import reframe.utility.sanity as sn
import os # For path joining

@rfm.simple_test
class OSUBandwidthSameSocketDiffNUMA(rfm.RunOnlyRegressionTest):
    valid_systems = ['aion', 'iris']  # Ensure Iris topology is compatible or adjust
    valid_prog_environs = ['foss', 'easybuild', 'eessi']
    time_limit = '10m'
    num_tasks = 2
    num_tasks_per_node = 2  # This ensures both tasks are on the same node
    message_size_bytes = 1048576
    # Core 0 is on Socket 0, NUMA Node 0.
    # Core 48 is on Socket 0, NUMA Node 3.
    cpu_cores_to_pin = "0,48" # Task 0 to core 0, Task 1 to core 48

    tags = {'osu', 'bandwidth', 'same_socket', 'diff_numa'}

    @run_before('run')
    def setup_test_executable_and_opts(self):
        env = self.current_environ.name
        self.descr = (f'osu_bw ({env}) on same socket, different NUMA nodes '
                      f'(cores {self.cpu_cores_to_pin})'
	f'(cores {self.cpu_cores_to_pin}), MsgSize: {self.message_size_bytes}B') # Updated descr
        self.executable_opts = [f'-m', f'{self.message_size_bytes}:{self.message_size_bytes}']
        self.executable_opts = ['-m', '1048576:1048576'] 

        if env == 'foss':
            user_home = os.path.expanduser('~')
            self.executable = os.path.join(user_home, 'hpc_software_project/osu_src/osu_bw')
        else:
            self.executable = 'osu_bw'

    @run_before('run')
    def set_slurm_options(self):
        self.job.options = ['--nodes=1', '--exclusive']
        self.job.launcher.options = [f'--cpu-bind=map_cpu:{self.cpu_cores_to_pin}']

    @sanity_function
    def check_run(self):
        return sn.assert_found(r'^1048576\s+\d+\.\d+', self.stdout)
    

    @performance_function('MB/s')
    def bandwidth(self):
        return sn.extractsingle(r'^1048576\s+(\S+)', self.stdout, 1, float)
