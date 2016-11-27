# taskflow_visualizer


## What is this?

Proof of concept for visualizing the [Openstack TaskFlow](https://wiki.openstack.org/wiki/TaskFlow) persistence backend using React.js and vis.js.

Don't mind the substandard code and lack of tests, this was just a small project to familiarize myself with a modern Javascript toolchain over the weekend.

Stuff:
- [Django](https://www.djangoproject.com/)
- [django-webpack-reloader](http://owaislone.org/blog/webpack-plus-reactjs-and-django/)
- [webpack](https://webpack.github.io/)
- [React.js](https://facebook.github.io/react/)
- [Vis.js](http://visjs.org/)


## Looks like

&nbsp;

<p align="center">
  <img
src="https://raw.githubusercontent.com/vdloo/taskflow_visualizer/master/docs/assets/creating_fixture.gif"
alt="flow execution example"/>
</p>

&nbsp;

<p align="center">
  <img
src="https://raw.githubusercontent.com/vdloo/taskflow_visualizer/master/docs/assets/view_logbook.gif"
alt="graph visualization example"/>
</p>


## Running

Make sure you have the requirements installed
```
node, npm, make, python3, pip
```

Run the server
```bash
make  # Install the dependencies and generate a fixture
make run  # Run the webserver
```

You can then manually re-run the flow simulation using
```bash
venv/bin/python scripts/create_fixture_data.py
```

And watch the following URL in the browser:
```bash
http://localhost:8009/graph/
```
