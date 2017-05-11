FROM_FORMAT=markdown
TO_FORMAT=html5

all: docs

docs:
	pandoc Readme.md -f $(FROM_FORMAT) -t $(TO_FORMAT) -s -o Readme.html

clean:
	rm Readme.html
