import reframe as rfm
import reframe.utility.sanity as sn
import os

@rfm.simple_test
class OSULatencySameSocketDiffNUMA(rfm.RunOnlyRegressionTest):
    valid_systems = ['aion:batch'] # Initially focus on Aion
    valid_prog_environs = ['foss', 'easybuild', 'eessi']
    time_limit = '10m'
    num_tasks = 2
    num_tasks_per_node = 2
    tags = {'osu', 'latency', 'same_socket_diff_numa'}

    # --- You MUST determine these values from hwloc on Aion ---
    CORE_MAP_AION = 'map_cpu:PUT_CORE_ID_A_HERE,PUT_CORE_ID_B_HERE' # Same as for bandwidth
    # CORE_MAP_IRIS = 'map_cpu:IRIS_CORE_ID_A,IRIS_CORE_ID_B' # If applicable for Iris


    @run_after('init')
    def set_executable_and_opts(self):
        self.executable_opts = ['-m', '8192:8192'] # 8192 bytes message size

    @run_before('run')
    def set_source_specific_exec(self):
        env_name = self.current_environ.name
        if env_name == 'foss':
            self.executable = os.path.join(self.prefix, 'osu_src', 'mpi', 'pt2pt', 'osu_latency')
            # Or the fixed path:
            # self.executable = '/mnt/aiongpfs/users/amahzoun/hpc_software_project/osu_src/mpi/pt2pt/osu_latency'
        else:
            self.executable = 'osu_latency'

    @run_before('run')
    def pin_tasks(self):
        self.descr = f'osu_latency ({self.current_environ.name}) on same socket, different NUMA nodes'
        self.job.launcher.options = ['--nodes=1']

        if self.current_system.name == 'aion':
            if self.CORE_MAP_AION == 'map_cpu:PUT_CORE_ID_A_HERE,PUT_CORE_ID_B_HERE':
                self.skip(f"Core IDs for Aion not set in the test. Please run hwloc.")
            self.job.launcher.options.append(f'--cpu-bind={self.CORE_MAP_AION}')
        elif self.current_system.name == 'iris':
            self.skip(f"Same socket, different NUMA test may not be applicable or configured for Iris. Please verify with hwloc.")
        else:
            self.skip(f"CPU binding not configured for system {self.current_system.name}")

    @sanity_function
    def check_run(self):
        # OSU prints '# OSU MPI Latency Test vX.Y'
        # Then a header, then data lines like: '8192          2.35'
        return sn.assert_found(r'^8192\s+\d+(\.\d+)?', self.stdout)

    @performance_function('us') # micro-seconds
    def latency(self):
        return sn.extractsingle(r'^8192\s+(\S+)', self.stdout, 1, float)

    @run_before('performance')
    def set_references(self):
        # These are initial guesses. Latency on same socket, diff NUMA should be
        # low, slightly higher than same NUMA, much lower than inter-node.
        # Aion typical intra-node: ~2.3 µs. This might be ~2.5-3.0 µs
        references = {
            'aion:batch': {
                'foss': {'latency': (2.8, -0.15, 0.15, 'us')},
                'easybuild': {'latency': (2.8, -0.15, 0.15, 'us')},
                'eessi': {'latency': (2.8, -0.15, 0.15, 'us')},
            },
        }
        sys_name = self.current_system.name
        part_name = self.current_partition.name
        env_name = self.current_environ.name
        
        ref_key = f'{sys_name}:{part_name}'
        if ref_key in references and env_name in references[ref_key]:
            self.reference = {f'{sys_name}:{part_name}': references[ref_key][env_name]}
        else:
            self.reference = {'*': {'latency': (0, None, None, 'us')}} # Fallback
            self.skip(f"No reference values defined for {ref_key} with {env_name} for this test.")
