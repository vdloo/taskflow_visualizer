var React = require('react')
var ReactDOM = require('react-dom')
var axios = require('axios');
var vis = require('vis');


var options = {
    width: (window.innerWidth - 25) + "px",
    height: (window.innerHeight - 75) + "px",
    physics: {
        stabilization: {
            enabled: true,
        }
    }
};


var graph_data = {
    nodes: new vis.DataSet([]),
    edges: new vis.DataSet([])
};

if (document.getElementById('network_graph')) {
    class VisNetwork extends React.Component {
      constructor(props) {
        super(props);

        this.state = {
          graph_data: [],
          network: new vis.Network(document.getElementById('canvas'), graph_data, options)
        };
      }

      componentDidMount(){
        setInterval(function() {
          axios.get(window.location.href.replace('graph', 'flows'))
            .then(res => {
              var nodes = [];
              var edges = [];
              var node_counter = 0;
              const logbooks = res.data.logbooks;
              Object.keys(logbooks).forEach(function(l_key) {
                  var logbook = logbooks[l_key];
                  node_counter++;
                  var logbook_node = node_counter;
                  nodes.push({
                      id: node_counter,
                      label: logbook.name
                  });

                  Object.keys(logbook.flow_details).map(function(f_key) {
                      var flow_detail = logbook.flow_details[f_key]
                      if (flow_detail.state != 'SUCCESS' && flow_detail.state != 'REVERTED' && flow_detail.state != 'FAILURE') {
                          node_counter++;
                          var flow_detail_node = node_counter;
                          nodes.push({
                              id: node_counter,
                              label: flow_detail.meta.factory.name
                          });
                          edges.push({
                              from: logbook_node,
                              to: flow_detail_node
                          });
                          var atomComponents = Object.keys(flow_detail.atom_details).map(function(a_key) {
                              var atom = flow_detail.atom_details[a_key];
                              node_counter++;
                              var atom_node = node_counter;
                              nodes.push({
                                  id: node_counter,
                                  label: atom.name
                              });
                              edges.push({
                                  from: flow_detail_node,
                                  to: atom_node
                              });
                          }.bind(this));
                      }
                  }.bind(this));


              }.bind(this));
              graph_data.nodes = new vis.DataSet(nodes);
              graph_data.edges = new vis.DataSet(edges);

              this.setState({ graph_data });
            });
        }.bind(this), 200);
      }

      render() {
        this.state.network.setData({ nodes: this.state.graph_data.nodes, edges: this.state.graph_data.edges });
        return <div></div>;
      }
    }

    ReactDOM.render(
        <VisNetwork />,
        document.getElementById('network_graph')
    );
}

if (document.getElementById('job_list')) {
    class TaskflowJobs extends React.Component {
      constructor(props) {
        super(props);

        this.state = {
          logbooks: []
        };
      }

      componentDidMount() {
        setInterval(function() {
          axios.get(window.location.href + 'flows/')
            .then(res => {
              const logbooks = res.data.logbooks;
              this.setState({ logbooks });
            });
        }.bind(this), 1000);
      }

      render() {
        var logbookComponents = Object.keys(this.state.logbooks).map(function(l_key) {
            var logbook = this.state.logbooks[l_key];
            var flowComponents = Object.keys(logbook.flow_details).map(function(f_key) {
                var flow = logbook.flow_details[f_key];
                if (flow.state != 'SUCCESS' && flow.state != 'REVERTED' && flow.state != 'FAILURE') {
                  var atomComponents = Object.keys(flow.atom_details).map(function(a_key) {
                      var atom = flow.atom_details[a_key];
                      return (
                          <li key={a_key}>{atom.name} {atom.state}</li>
                      )
                  }.bind(this));
                  return (
                      <li key={f_key}>{flow.uuid} {flow.state}
                      <ul>
                      {atomComponents}
                      </ul>
                      </li>
                  )
                }
            }.bind(this));

            return (
            <li key={l_key}>
            {logbook.name}
            <ul>
            {flowComponents}
            </ul>
            </li>
        );
        }.bind(this));
        return (
          <div>
            <h1>Logbooks</h1>
            <ul>
            {logbookComponents}
            </ul>
          </div>
        );
      }
    }
    ReactDOM.render(
        <TaskflowJobs />,
        document.getElementById('job_list')
    );
}
