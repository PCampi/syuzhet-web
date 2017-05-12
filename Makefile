FROM_FORMAT=markdown
TO_FORMAT=html5

all: docs

docs: clean
	@echo 'Rebuilding Readme.html'
	pandoc Readme.md -f $(FROM_FORMAT) -t $(TO_FORMAT) -s -o static/Readme.html

clean:
	@echo 'Cleaning'
	@if [ -f static/Readme.html ]; then rm static/Readme.html ; fi
