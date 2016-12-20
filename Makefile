all: clean venv test sdist

clean:
	find gphoto_backup -type f -name *.pyc | xargs rm -rf
	find gphoto_backup -type d -name __pycache__ | xargs rm -rf
	rm -rf coverage
	rm -f .coverage
	rm -rf dist
	rm -f MANIFEST
	rm -rf gphoto_backup.egg-info/

venv2:
	rm -rf ./.venv2/
	virtualenv --python=python2.7 .venv2
	.venv2/bin/pip install -r dev-requirements.txt

# venv3:
# 	rm -rf ./.venv3/
# 	virtualenv --python=python3 .venv3
# 	.venv3/bin/pip install -r dev-requirements.txt

venv: venv2 #venv3

test2:
# 	.venv2/bin/nosetests

# test3:
# 	.venv3/bin/nosetests

test: test2 #test3

cover:
	.venv2/bin/nosetests --with-coverage --cover-branches --cover-package=gphoto_backup --cover-html --cover-html-dir=coverage

run:
	bin/gphoto_backup

doc:
	rm -f README
	pandoc README.md -o README -w rst

sdist2: clean doc
	python2.7 setup.py sdist

# sdist3: clean doc
# 	python3 setup.py sdist

sdist: sdist2# sdist3

install: sdist2
	pip install dist/gphoto_backup-*.tar.gz ${ARGS}
	rm -rf dist

uninstall:
	pip uninstall gphoto_backup

publish: sdist
	twine upload dist/*
