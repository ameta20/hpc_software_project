Setup Instruction

    Connect to Iris or Aion cluster using your credentials
    Clone the repository to your Home directory
    Connect to a compute node using si command (e.g. si -t 1:00:00)
    (Note that adding some args may cause error)
    Run the shell script run.sh (./run.sh).

Files Structure
-- config
      -- ulhpc.py
-- Makefile
-- README.md
-- reframe_tests
      -- osu_bw_diff_nodes.py
      -- [Other tests]...
-- run.sh