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

server:
	python server.py

install:
	npm install
	python -m pip install -r ./requirements.txt

deploy:
	git subtree push --prefix roadmap-to-html origin gh-pages

	git push origin `git subtree split --prefix roadmap-to-html master`:gh-pages --force