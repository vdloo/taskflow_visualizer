var React = require('react')
var ReactDOM = require('react-dom')
var axios = require('axios');

var Hello = React.createClass ({
    render: function() {
        return (
            <h1>
            Hello, React!
            </h1>
        )
    }
})

ReactDOM.render(<Hello />, document.getElementById('container'))