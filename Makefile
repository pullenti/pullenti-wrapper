
tag:
	git tag `python version.py get setup.py`

version:
	python version.py inc setup.py

wheel:
	python setup.py bdist_wheel

upload:
	twine upload dist/*

test:
	pytest --pep8 --flakes pullenti_wrapper --nbval-lax -v docs.ipynb

clean:
	find pullenti_wrapper -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info
