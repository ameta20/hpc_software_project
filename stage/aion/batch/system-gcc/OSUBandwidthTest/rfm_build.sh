#!/bin/bash

_onerror()
{
    exitcode=$?
    echo "-reframe: command \`$BASH_COMMAND' failed (exit code: $exitcode)"
    exit $exitcode
}

trap _onerror ERR

export EASYBUILD_BUILDPATH=/mnt/aiongpfs/users/ameta/hpc_software_project/stage/aion/batch/system-gcc/OSUBandwidthTest/easybuild/build
export EASYBUILD_INSTALLPATH=/mnt/aiongpfs/users/ameta/hpc_software_project/stage/aion/batch/system-gcc/OSUBandwidthTest/easybuild
export EASYBUILD_PREFIX=/mnt/aiongpfs/users/ameta/hpc_software_project/stage/aion/batch/system-gcc/OSUBandwidthTest/easybuild
export EASYBUILD_SOURCEPATH=/mnt/aiongpfs/users/ameta/hpc_software_project/stage/aion/batch/system-gcc/OSUBandwidthTest/easybuild
eb OSU-Micro-Benchmarks-7.2-gompi-2023.09.eb 
