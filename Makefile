TARGETS = README.md formulas-ascii.md demo-ascii.csv demo-unicode.csv debug-ascii.csv debug-unicode.csv

.PHONY: $(TARGETS)

all: $(TARGETS)

README.md:
	python compile.py -t README.md -c unicode > README.md

formulas-ascii.md:
	python compile.py -t formulas.md -c ascii > formulas-ascii.md

demo-ascii.csv:
	python compile.py -t demo.csv -c ascii > demo-ascii.csv

demo-unicode.csv:
	python compile.py -t demo.csv -c unicode > demo-unicode.csv

debug-ascii.csv:
	python compile.py -t debug.csv -c ascii > debug-ascii.csv

debug-unicode.csv:
	python compile.py -t debug.csv -c unicode > debug-unicode.csv
