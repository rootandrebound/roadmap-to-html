# Roadmap to HTML

A github repo for code to convert the [Roadmap to Reentry](https://objects-us-west-1.dream.io/roadmapguide/RoadmapGuide-2016.pdf) into HTML.

### Getting started

#### 1. Clone this repo to your computer

```
git clone https://github.com/rootandrebound/roadmap-to-html.git
cd roadmap-to-html
```

#### 2. Get `2016-04-12_Final_st.docx`

To get started, you need to [download the original word document](https://drive.google.com/uc?export=download&id=0BzNrkiCWAqHZdDNzdlNlY2FKNVU) and put it in this folder. Note that the preceding link should only be accessible to staff members at Root & Rebound or people who have been given specific access to the containing folder.

#### 3. Install [mammoth](https://github.com/mwilliamson/mammoth.js)

You will need to have [`node`](https://nodejs.org/en/download/) installed if you don't already.

```
npm install
```

#### 4. Run the script to make HTML

```
make
```

This will produce an output similar to [what is described here](https://github.com/rootandrebound/roadmap-to-html/issues/1).

### The script

The Makefile includes one command for producing the HTML output:

```bash
node_modules/mammoth/bin/mammoth \  # the path to mammoth's executable
    2016-04-12_Final_st.docx \      # the path to the input word document
    --output-dir=roadmap \          # the output directory
    --style-map=stylemap.txt        # the stylemap
```

