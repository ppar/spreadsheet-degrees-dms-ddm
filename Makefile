.PHONY: README.md demo.csv debug.csv

all: README.md demo.csv debug.csv

README.md:
	python compile.py -readme > README.md

demo.csv:
	python compile.py -csv > demo.csv

debug.csv:
	python compile.py -csv-debug > debug.csv
