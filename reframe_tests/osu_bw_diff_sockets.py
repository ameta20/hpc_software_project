import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class OSUBandwidthDiffSockets(rfm.RunOnlyRegressionTest):
    valid_systems = ['aion', 'iris']
    valid_prog_environs = ['foss', 'easybuild', 'eessi']
    time_limit = '10m'
    num_tasks = 2
    num_tasks_per_node = 2
    tags = {'osu', 'bandwidth', 'diff_sockets'}

    @run_before('run')
    def setup_test(self):
        env = self.current_environ.name

        self.descr = f'osu_bw ({env}) on same node, different sockets'
        self.executable_opts = ['-m', '1048576:1048576']

        if env == 'foss':
            self.executable = '/mnt/aiongpfs/users/amahzoun/hpc_software_project/osu_src/osu_bw'
        else:
            self.executable = 'osu_bw'  # Expected to be in $PATH for easybuild/eessi

    @run_before('run')
    def pin_tasks_on_sockets(self):
        self.job.options += ['--ntasks-per-socket=1', '--nodes=1']

    @sanity_function
    def check_run(self):
        return sn.assert_found(r'^1048576\s+\d+', self.stdout)

    @performance_function('MB/s')
    def bandwidth(self):
        return sn.extractsingle(r'^1048576\s+(\S+)', self.stdout, 1, float)

