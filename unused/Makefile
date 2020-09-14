all: requirements.out yt_data rm_out

requirements.out: requirements.txt
	pip3 install -r $< > $@

yt_data: requirements.out
	python yt_download.py

rm_out: requirements.out
	rm $< 
