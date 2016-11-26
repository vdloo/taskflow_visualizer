.PHONY: all default run test clean

NAME := taskflow_visualizer
VERSION := 0.1
MAINTAINER := Rick van de Loo <rickvandeloo@gmail.com>
DESCRIPTION := Visualize the taskflow persistence backend

default:
	[ ! -d venv ] && virtualenv venv -p python3 || /bin/true
	venv/bin/pip install distribute --upgrade --quiet
	venv/bin/pip install -r requirements/base.txt
	npm install
	node_modules/.bin/webpack --config webpack.config.js
run:
	./manage.py makemigrations
	./manage.py migrate
	./manage.py runserver 8009
test:
	./runtests.sh -1
clean:
	git clean -xfd
