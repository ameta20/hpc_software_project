import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class OSUBandwidthSameSocketDiffNUMA(rfm.RunOnlyRegressionTest):
    valid_systems = ['aion:batch'] 
    valid_prog_environs = ['foss', 'easybuild', 'eessi']
    time_limit = '10m'
    num_tasks = 2
    num_tasks_per_node = 2
    tags = {'osu', 'bandwidth', 'same_socket_diff_numa'}

    CORE_MAP_AION = 'map_cpu:0,48'


    @run_after('init') 
    def set_executable_and_opts(self):
        self.executable_opts = ['-m', '1048576:1048576'] # 1MB message size

    def set_scheduler_options(self):
        self.job.sched_access = ['--exclusive']

    @run_before('run')
    def set_source_specific_exec(self):
        env_name = self.current_environ.name
        if env_name == 'foss':
            self.executable = '/mnt/aiongpfs/users/ameta/hpc_software_project/osu_src/mpi/pt2pt/osu_bw'
        else:
            self.executable = 'osu_bw'

    @run_before('run')
    def pin_tasks(self):
	self.descr = f'osu_bw ({self.current_environ.name}) on same socket, different NUMA nodes'
        srun_options = ['--nodes=1']
        srun_options.append('--cpus-per-task=1') 

        if self.current_system.name == 'aion':
            srun_options.append(f'--cpu-bind={self.CORE_MAP_AION}')
        elif self.current_system.name == 'iris':
            self.skip(f"Same socket, different NUMA test may not be applicable or configured for Iris. Please verify with hwloc.")
        else:
            self.skip(f"CPU binding not configured for system {self.current_system.name}")
        self.job.launcher.options = srun_options


    @sanity_function
    def check_run(self):
        # OSU prints '# OSU MPI Bandwidth Test vX.Y'
        # Then a header, then data lines like: '1048576       12345.67'
        return sn.assert_found(r'^1048576\s+\d+(\.\d+)?', self.stdout)

    @performance_function('MB/s')
    def bandwidth(self):
        return sn.extractsingle(r'^1048576\s+(\S+)', self.stdout, 1, float)

    @run_before('performance') # Set references after setup and before performance analysis
    def set_references(self):
        references = {
            'aion:batch': { # Specific to Aion
                'foss': {'bandwidth': (10000, -0.10, 0.10, 'MB/s')},
                'easybuild': {'bandwidth': (10000, -0.10, 0.10, 'MB/s')},
                'eessi': {'bandwidth': (10000, -0.10, 0.10, 'MB/s')},
            },
        }
