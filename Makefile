default:
	# converts Word docx to raw HTML
	node_modules/mammoth/bin/mammoth \
		--output-dir=output \
		--style-map=stylemap.txt \
		2017.02.18_Final.docx
	# renames the raw HTML
	mv output/2017.02.18_Final.html \
		output/raw_index.html
	# parses the raw HTML & rerenders the templates
	python main.py

server:
	python server.py

install:
	npm install
	python -m pip install -r ./requirements.txt

deploy:
	git subtree push --prefix output origin gh-pages
