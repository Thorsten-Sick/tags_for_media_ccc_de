# Makefile to get a standard command set to all my projects. No matter which tech they got developed with

.PHONY: bootstrap, teardown, enter, leave


# Set up build environment, install dependencies
bootstrap: requirements.txt
	test -d virtenv || virtualenv -p python3 virtenv
	. virtenv/bin/activate; pip install -Ur requirements.txt
	touch virtenv/bin/activate

# remove build environment
teardown:
	rm -rf virtenv
	find -iname "*.pyc" -delete

clean:
	find -iname "*.pyc" -delete		

enter:
	echo "Call: . virtenv/bin/activate"

leave:
	echo "Call: deactivate"

# TODO
test:
	. virtenv/bin/activate; # ... run test here ...

# TODO
release:
	. virtenv/bin/activate; # Make release
