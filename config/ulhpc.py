site_configuration = {
    'systems': [
        {
            'name': 'aion',
            'descr': 'Aion cluster',
            'hostnames': [r'aion-[0-9]{4}'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'batch',
                    'descr': 'Aion compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['--partition=batch', '--qos=normal'],
                    'max_jobs':  8,
                    'environs': ['foss', 'easybuild', 'eessi'],
                }
            ]
        },
        {
            'name': 'iris',
            'descr': 'Iris cluster',
            'hostnames': [r'iris-[0-9]{3}'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'batch',
                    'descr': 'Iris compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['--partition=batch', '--qos=normal'],
                    'max_jobs':  8,
                    'environs': ['foss', 'easybuild', 'eessi'],
                }
            ]
        }
    ],
    'environments': [
    {
        'name': 'foss',
        'modules': ['env/release/default', 'toolchain/foss/2023b'],
        'cc': 'mpicc',
        'cxx': 'mpic++',
        'ftn': 'mpif90',
        'target_systems': ['iris', 'aion']
    },
    {
        'name': 'easybuild',
        'modules': [
            'env/release/default',
            'toolchain/gompi/2023b',
            'perf/OSU-Micro-Benchmarks/7.5-gompi-2023b'
        ],
        'cc': 'mpicc',
        'cxx': 'mpic++',
        'ftn': 'mpif90',
        'target_systems': ['iris', 'aion']
    },
    {
        'name': 'eessi',
        'modules': [
            'env/release/default',
            'mpi/OpenMPI/4.1.6-GCC-13.2.0',
            'EESSI/2023.06',
            'OSU-Micro-Benchmarks/7.2-gompi-2023b'
        ],
        'cc': 'mpicc',
        'cxx': 'mpic++',
        'ftn': 'mpif90',
        'target_systems': ['iris', 'aion']
    },
]}
