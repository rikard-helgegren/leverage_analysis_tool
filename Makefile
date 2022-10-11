
all: code/compiled_code run

debug: code/compiled_code debug_run

info: code/compiled_code info_run

clean:
	rm -rf code/compiled_code

code/compiled_code:
	mkdir code/compiled_code
	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$0/model
	python3 code/setup.py

run:
	python3 leverage_analysis_tool.py

debug_run:
	python3 leverage_analysis_tool.py -debug

info_run:
	python3 leverage_analysis_tool.py -info