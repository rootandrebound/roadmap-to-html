default:
	node_modules/mammoth/bin/mammoth \
		--output-dir=output \
		--style-map=stylemap.txt \
		2017.02.18_Final.docx
	mv output/2017.02.18_Final.html \
		output/raw_index.html
	python main.py


install:
	npm install
	pip install -r ./requirements.txt
