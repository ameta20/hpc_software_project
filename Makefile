SRC_DIR := src
OSU_VERSION := 7.5
OSU_TARBALL := osu-micro-benchmarks-$(OSU_VERSION).tar.gz
OSU_DIR := osu-micro-benchmarks-$(OSU_VERSION)
BUILD_DIR := $(OSU_DIR)/c/mpi/pt2pt/standard

all:
	@echo -e "\033[1;31;43mAvailable options:				\033[0m"
	@echo -e "\033[31;43m  make generate_osu_executables_from_source	\033[0m"
	@echo -e "\033[31;43m  make clean_osu_executables			\033[0m"

generate_osu_executables_from_source:
	mkdir -p $(SRC_DIR)
	wget -nc https://mvapich.cse.ohio-state.edu/download/mvapich/$(OSU_TARBALL)
	tar -xf $(OSU_TARBALL)
	cd $(OSU_DIR) && ./configure CC=mpicc --prefix=$(abspath $(SRC_DIR))
	$(MAKE) -C $(BUILD_DIR) osu_bw osu_latency
	cp $(BUILD_DIR)/osu_bw $(SRC_DIR)/
	cp $(BUILD_DIR)/osu_latency $(SRC_DIR)/
	rm -rf $(OSU_DIR) $(OSU_TARBALL)

clean_osu_executables:
	rm -f $(SRC_DIR)/osu_bw.c $(SRC_DIR)/osu_latency.c

