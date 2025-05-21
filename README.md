# hpc_software_project


### Setup Instruction
1. Connect to Iris or Aion cluster using your credentials
1. Clone the repository to your Home directory
2. Connect to a compute node using si command (e.g. si -t 1:00:00)  
(Note that adding some args may cause error)
3. Run the shell script run.sh (./run.sh).


### Files Structure
-- config
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-- ulhpc.py
-- Makefile
-- README.md
-- reframe_tests
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-- osu_bw_diff_nodes.py
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-- [Other tests]...
-- run.sh
