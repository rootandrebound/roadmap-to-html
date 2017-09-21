default:
	# converts Word docx to raw HTML
	node_modules/mammoth/bin/mammoth \
		--output-dir=roadmap-to-html/ \
		--style-map=stylemap.txt \
		./source.docx
	# renames the raw HTML
	mv roadmap-to-html/source.html \
		roadmap-to-html/raw_index.html
	# parses the raw HTML & rerenders the templates
	python main.py
	#create js and css bundles
	gulp sass
	gulp js

server:
	gulp
	# todo remove python server dependencies

install:
	npm install
	python -m pip install -r ./requirements.txt

deploy:
	git subtree push --prefix output origin gh-pages
