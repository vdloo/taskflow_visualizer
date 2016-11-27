var React = require('react')
var ReactDOM = require('react-dom')
var axios = require('axios');


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
              console.log(flow);
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
  document.getElementById('container')
);
