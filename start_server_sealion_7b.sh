export ONEDNN_MAX_CPU_ISA=AVX512_CORE_AMX
#export ONEDNN_MAX_CPU_ISA=AVX512_CORE_VNNI
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so
export MALLOC_CONF="oversize_threshold:1,background_thread:true,metadata_thp:auto,dirty_decay_ms:60000,muzzy_decay_ms:-1"
export OMP_NUM_THREADS=112
export no_proxy=localhost,127.0.0.1,*.intel.com

# uvicorn server_stream:app --reload
numactl -C 0-55,112-167 python3 server_stream_bigdl_Sealion.py -m "sea-lion-7b-instruct"


