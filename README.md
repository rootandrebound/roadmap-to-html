# Roadmap to HTML

A github repo for code to convert the [Roadmap to Reentry](https://objects-us-west-1.dream.io/roadmapguide/RoadmapGuide-2016.pdf) into HTML.

## Before you start

Make sure you have [node](https://nodejs.org/en/download/) and [python3](https://www.python.org/downloads/) installed.

## Getting started


### Quickstart

An outline of commands used, for people who are comfortable on the command line:

``` bash
git clone https://github.com/rootandrebound/roadmap-to-html.git
cd roadmap-to-html
python3 -m venv .    # create a python virtual environment
source bin/activate  # activate the virtual environment
make install         # install all node and python dependencies
make                 # build the output
```


### 1. Clone this repo to your computer

```bash
git clone https://github.com/rootandrebound/roadmap-to-html.git
cd roadmap-to-html
```

### 2. Get the latest version of the Word document (`source.docx`)

To get started, you need to [download the original word document](https://drive.google.com/uc?export=download&id=0BzNrkiCWAqHZdDNzdlNlY2FKNVU) and put it in the root project folder. Download `source.docx` and put it in the root folder for this repository.
Note that the preceding link should only be accessible to staff members at Root & Rebound or people who have been given specific access to the containing folder.

### 3. Create and activate a python virtual environment

This step ensures that any python dependencies will not interfere with other Python projects on your computer. This step is a common good practice when working on any project that uses Python.

```bash
python3 -m venv .    # create a python virtual environment
source bin/activate  # activate the virtual environment
```

### 3. Install dependencies

This command will install all the dependencies for both Node and Python.
```bash
make install
```

### 4. Run the script to make HTML

This command will:
- Produce an output similar to [what is described here](https://github.com/rootandrebound/roadmap-to-html/issues/1).
- Run the necesary gulp tasks to compile and minify CSS & Javascript

```bash
make
```

### 5. View the HTML locally

This command will fire up a development server and you will be able to see the site opening http://localhost:3000/ in your browser.

```bash
make server
```

### The script

The Makefile includes one command for producing the HTML output:

```bash
node_modules/mammoth/bin/mammoth \  # the path to mammoth's executable
    ./source.docx \      # the path to the input word document
    --output-dir=roadmap \          # the output directory
    --style-map=stylemap.txt        # the stylemap
    mv output/source.html \  # rename the resulting html doc
        output/raw_index.html
    python main.py                  # chop up and output each chapter
```
