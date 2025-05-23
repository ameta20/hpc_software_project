#!/bin/bash

# Load Modules
module load toolchain/foss/2023b
module load devel/ReFrame/4.7.4-GCCcore-13.2.0

# Generate OSU Executables from source
if [ ! -d "osu_src" ]; then
  echo "Directory osu_src does not exist. Running command..."
  make generate_osu_executables_from_source
else
  echo "Directory osu_src already exists."
fi

# Run Tests
echo "================================== SAME_NUMA_BW =================================="
reframe -C config/ulhpc.py -c reframe_tests/osu_bw_same_numa.py -r
echo "================================ SAME_NUMA_LATENCY =================================="
reframe -C config/ulhpc.py -c reframe_tests/osu_latency_same_numa.py -r
echo "================================== DIFF_NUMA_BW =================================="
reframe -C config/ulhpc.py -c reframe_tests/osu_bw_same_socket_diff_numa.py -r
echo "================================ DIFF_NUMA_LATENCY =================================="
reframe -C config/ulhpc.py -c reframe_tests/osu_latency_same_socket_diff_numa.py -r
echo "================================== DIFF_SOCKETS_BW =================================="
reframe -C config/ulhpc.py -c reframe_tests/osu_bw_diff_sockets.py -r
echo "================================ DIFF_SOCKETS_LATENCY =================================="
reframe -C config/ulhpc.py -c reframe_tests/osu_latency_diff_sockets.py -r
echo "================================== DIFF_NODES_BW =================================="
reframe -C config/ulhpc.py -c reframe_tests/osu_bw_diff_nodes.py -r
echo "================================ DIFF_NODES_LATENCY =================================="
reframe -C config/ulhpc.py -c reframe_tests/osu_latency_diff_nodes.py -r
