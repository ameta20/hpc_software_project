# config/systems.py
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
                    'environs': ['foss', 'system-gcc'],
                }
            ]
        }
    ],
    'environments': [
        {
            'name': 'foss',
            'modules': ['toolchain/foss/2023b'],
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'target_systems': ['aion']
        },
        {
            'name': 'system-gcc',
            'cc': 'mpicc',
            'cxx': 'mpicxx',
            'target_systems': ['aion']
        },
    ]
}
