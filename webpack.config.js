var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    context: __dirname,
    entry: './taskflow_visualizer/static/js/index', 
    
    output: {
        path: path.resolve('./taskflow_visualizer/static/js/bundles/'), 
        filename: '[name]-[hash].js', 
    },
    
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}), 
        new webpack.ProvidePlugin({ 
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery' 
        })
    ],
    
    module: {
        loaders: [
            {test: /\.jsx?$/, 
                exclude: /node_modules/, 
                loader: 'babel-loader', 
                query: {
                    presets: ['react'] 
                }
            }
        ]
    },
    
    resolve: {
        modulesDirectories: ['node_modules'],
        extensions: ['', '.js', '.jsx'] 
    }   
}
