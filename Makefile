test:
	coverage run tests.py

verify:
	pyflakes main.py structures.py
	pep8 --ignore=E128 main.py structures.py

clean:
	find . -name *.pyc -delete

profile:
	python profile.py
