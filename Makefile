
version:
	bumpversion minor

wheel:
	python setup.py bdist_wheel

upload:
	twine upload dist/*

test:
	pytest --pep8 --flakes pullenti_wrapper -v --nbval-lax --current-env docs.ipynb docs.ipynb

clean:
	find pullenti_wrapper -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info
