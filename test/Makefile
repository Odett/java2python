javac := javac
java := java
python := python -B
j2py = ../bin/j2py


python_files := $(addsuffix .py, $(notdir $(basename $(wildcard *.java))))
test_targets := $(sort $(notdir $(basename $(wildcard *.java))))


.PHONY: all clean
.SILENT: %:


all:
	$(MAKE) $(test_targets)
	@cd selector && make


clean:
	@rm -f *.class *.pyc $(python_files)


packages:
	@cd Package1 && javac Class1.java
	@cd Package1 && ../$(j2py) -i Class1.java  -o Class1.py


parsers:
	@cd ../java2python/lang && make -s


%.class:
	[ -s $(addsuffix .java, $(basename $@)) ] && $(javac) $(addsuffix .java, $(basename $@))


%.py: %.class
	@$(j2py) -i $(addsuffix .java, $(basename $@)) -o $@ -c configs/__init__.py -d configs

%: %.py
	@bash -c "diff -q <($(python) $(addsuffix .py, $@)) <(java -ea $@)" && echo "[PASS] $@"
