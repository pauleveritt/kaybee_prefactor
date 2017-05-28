const webpack = require('webpack')
const path = require('path')

const ExtractTextPlugin = require('extract-text-webpack-plugin')
const extractCSS = new ExtractTextPlugin('[name].bundle.css')

const config = {
    context: path.resolve(__dirname, 'kaybee'),
    entry: {
        basic: './app.js'
    },
    output: {
        path: path.resolve(__dirname, 'kaybee/static'),
        publicPath: '/static/',
        filename: '[name].bundle.js'
    },
    devServer: {
        // contentBase: path.resolve(__dirname, './src')
    },
    module: {
        rules: [
            {
                test: /\.(png|jpg)$/,
                include: path.resolve(__dirname, 'kaybee'),
                use: [
                    {
                        loader: 'url-loader',
                        options: {limit: 10000} // Convert images < 10k to base64 strings
                    }]
            },
            {
                test: /\.scss$/,
                include: path.resolve(__dirname, 'kaybee'),
                loader: extractCSS.extract(['css-loader', 'sass-loader'])
            },
            {
                test: /\.js$/,
                include: path.resolve(__dirname, 'kaybee'),
                use: [{
                    loader: 'babel-loader',
                    options: {presets: ['es2015']}
                }]
            }]
    },
    plugins: [
        new webpack.optimize.CommonsChunkPlugin({
            names: ['vendor', 'manifest'],
            minChunks: function (module) {
                // this assumes your vendor imports exist in the node_modules directory
                return module.context && module.context.indexOf('node_modules') !== -1
            }
        }),
        extractCSS,
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            'Tether': 'tether'
        })
    ]
}

module.exports = config
