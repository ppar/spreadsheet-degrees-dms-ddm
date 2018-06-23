TARGETS = README.md formulas-ascii.md demo-ascii.csv demo-unicode.csv debug-ascii.csv debug-unicode.csv

.PHONY: $(TARGETS)

all: $(TARGETS)

README.md:
	python compile.py README.md > README.md

formulas-ascii.md:
	python compile.py formulas-ascii.md > formulas-ascii.md

demo-ascii.csv:
	python compile.py demo-ascii.csv > demo-ascii.csv

demo-unicode.csv:
	python compile.py demo-unicode.csv > demo-unicode.csv

debug-ascii.csv:
	python compile.py debug-ascii.csv > debug-ascii.csv

debug-unicode.csv:
	python compile.py debug-unicode.csv > debug-unicode.csv
