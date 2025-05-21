import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class OSULatencyDiffSockets(rfm.RunOnlyRegressionTest):
    valid_systems = ['aion', 'iris']
    valid_prog_environs = ['foss', 'easybuild', 'eessi']
    time_limit = '10m'
    num_tasks = 2
    num_tasks_per_node = 2
    tags = {'osu', 'latency', 'diff_sockets'}

    @run_before('run')
    def setup_test(self):
        env = self.current_environ.name

        self.descr = f'osu_latency ({env}) on same node, different sockets'
        self.executable_opts = ['-m', '8192:8192']
        
        if env == 'foss':
            import os
            user_home = os.path.expanduser('~')  # Gets the user's home directory
            self.executable = os.path.join(user_home, 'hpc_software_project/osu_src/osu_latency')
        else:
            self.executable = 'osu_latency'  # Expected to be in $PATH for easybuild/eessi

    @run_before('run')
    def pin_tasks_on_sockets(self):
        self.job.options += ['--ntasks-per-socket=1', '--nodes=1']

    @sanity_function
    def check_run(self):
        return sn.assert_found(r'^8192\s+\d+', self.stdout)

    @performance_function('us')
    def latency(self):
        return sn.extractsingle(r'^8192\s+(\S+)', self.stdout, 1, float)
