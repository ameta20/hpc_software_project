@rfm.simple_test
class OSULatencyDiffSockets(rfm.RunOnlyRegressionTest):
    binary_source = parameter(['source', 'easybuild', 'eessi'])

    valid_systems = ['*']
    valid_prog_environs = ['*']
    time_limit = '10m'
    num_tasks = 2
    num_tasks_per_node = 2
    tags = {'osu', 'latency', 'diff_sockets'}

    @run_after('init')
    def setup_test(self):
        self.descr = f'osu_latency ({self.binary_source}) on same node, different sockets'
        self.executable_opts = ['-m', '8192:8192']
        
        if self.binary_source == 'source':
            self.modules = ['toolchain/foss/2023b']
            self.pre_run = [
                'module load toolchain/foss/2023b',
                'mpicc src/osu_latency.c -o osu_latency'
            ]
            self.executable = './osu_latency'
        elif self.binary_source == 'easybuild':
            self.modules = ['perf/OSU-Micro-Benchmarks/7.5-gompi-2023b']
            self.executable = 'osu_latency'
        elif self.binary_source == 'eessi':
            self.modules = ['EESSI/2023.06']
            self.executable = 'osu_latency'

        self.job.options += ['--map-by', 'socket']

    @sanity_function
    def check_run(self):
        return sn.assert_found(r'^8192\s+\d+', self.stdout)

    @performance_function('us')
    def latency(self):
        return sn.extractsingle(r'^8192\s+(\S+)', self.stdout, 1, float)

    @run_after('setup')
    def set_references(self):
        self.reference = {
            '*': {
                'latency': (2.3, -0.15, 0.15, 'us')
            }
        }
