import reframe as rfm
import reframe.utility.sanity as sn
import subprocess

@rfm.simple_test
class OSUBandwidthSameNUMAAuto(rfm.RunOnlyRegressionTest):
    valid_systems = ['aion', 'iris']
    valid_prog_environs = ['foss', 'easybuild', 'eessi']
    time_limit = '10m'
    num_tasks = 2
    num_tasks_per_node = 2
    tags = {'osu', 'bandwidth', 'same_numa'}
    cpu_cores_to_pin = "0,2"

    @run_before('run')
    def setup_test(self):
        env = self.current_environ.name
        self.descr = f'osu_bw ({env}) on the same NUMA node (auto core selection)'
        self.executable_opts = ['-m', '1048576:1048576']
        if env == 'foss':
            import os
            user_home = os.path.expanduser('~')  # Gets the user's home directory
            self.executable = os.path.join(user_home, 'hpc_software_project/osu_src/osu_bw')    
        else:
            self.executable = 'osu_bw'

    @run_before('run')
    def set_slurm_options(self):
        self.job.options = ['--nodes=1', '--exclusive']

        self.job.launcher.options = [f'--cpu-bind=map_cpu:{self.cpu_cores_to_pin}']


    @sanity_function
    def check_run(self):
        return sn.assert_found(r'^1048576\s+\d+', self.stdout)

    @performance_function('MB/s')
    def bandwidth(self):
        return sn.extractsingle(r'^1048576\s+(\S+)', self.stdout, 1, float)

