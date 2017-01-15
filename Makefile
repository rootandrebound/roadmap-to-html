default:
	node_modules/mammoth/bin/mammoth \
		--output-dir=output \
		--style-map=stylemap.txt \
		2016-04-12_Final_st.docx
	mv output/2016-04-12_Final_st.html \
		output/raw_index.html
	python main.py


