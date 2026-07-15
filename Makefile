BUILD_DIR ?= build-m0dul0
TARGET ?= esp32
PORT ?= /dev/ttyUSB0
IDF_IMAGE ?= espressif/idf:release-v5.5

.PHONY: all build set-target flash monitor fullclean inspect docker-build

all: build

set-target:
	idf.py -B "$(BUILD_DIR)" set-target "$(TARGET)"

build:
	idf.py -B "$(BUILD_DIR)" build

flash:
	idf.py -B "$(BUILD_DIR)" -p "$(PORT)" flash

monitor:
	idf.py -B "$(BUILD_DIR)" -p "$(PORT)" monitor

fullclean:
	idf.py -B "$(BUILD_DIR)" fullclean

inspect:
	python3 tools/firmware_inspector.py \
		"$(BUILD_DIR)/ble_ctf.bin" \
		--partition-table "$(BUILD_DIR)/partition_table/partition-table.bin" \
		--hex20

docker-build:
	docker run --rm \
		-v "$(CURDIR)":/project -w /project \
		-u "$$(id -u):$$(id -g)" -e HOME=/tmp \
		"$(IDF_IMAGE)" \
		idf.py -B "$(BUILD_DIR)" set-target "$(TARGET)" build
