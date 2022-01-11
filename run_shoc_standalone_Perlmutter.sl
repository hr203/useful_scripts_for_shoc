#!/bin/bash
#SBATCH -N 1
#SBATCH -C gpu
#SBATCH -G 1
#SBATCH -t 10
#SBATCH -A nstaff_g

cd scream/components/scream/
mkdir -p build/test
cd build/test
module unload cray-hdf5-parallel cray-netcdf-hdf5parallel cray-parallel-netcdf PrgEnv-gnu PrgEnv-nvidia cuda craype-accel-host perftools-base perftools darshan
module load PrgEnv-gnu/8.2.0 gcc/9.3.0 cudatoolkit cray-libsci/21.08.1.2 craype cray-mpich cray-hdf5-parallel/1.12.0.7 cray-netcdf-hdf5parallel/4.7.4.7 cray-parallel-netcdf/1.12.1.7 cmake
export NVCC_WRAPPER_DEFAULT_COMPILER="$(which CC)"
cmake -DCMAKE_Fortran_COMPILER=ftn -DCMAKE_C_COMPILER=cc -DCMAKE_CXX_COMPILER=/global/homes/h/hross/codes/scream/externals/ekat/extern/kokkos/bin/nvcc_wrapper -DMAKE_BUILD_TYPE=Debug -DKokkos_ENABLE_DEBUG=OFF -DEKAT_DEFAULT_BFB=ON -DKokkos_ENABLE_CUDA=ON -DKokkos_ENABLE_CUDA_LAMBDA=ON -DKokkos_ARCH_AMPERE80=ON -DKokkos_ENABLE_PROFILING=OFF -DKokkos_ENABLE_AGGRESSIVE_VECTORIZATION=OFF -DKokkos_ENABLE_DEPRECATED_CODE=OFF -DKokkos_ENABLE_EXPLICIT_INSTANTIATION=OFF -DSCREAM_FPE=OFF -DSCREAM_DOUBLE_PRECISION=OFF \../..
make -j8 
make baseline
cd tests/uncoupled/shoc
srun ./shoc_standalone >& ../../../../../../../../shoc_standalone_out

