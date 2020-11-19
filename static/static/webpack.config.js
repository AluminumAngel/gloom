const webpack = require( 'webpack' );

const config = {
  entry:  __dirname + '/js/index.jsx',
  output: {
    path: __dirname + '/dist',
    filename: 'bundle.js',
  },
  resolve: {
    extensions: [ '.js', '.jsx', '.css' ],
  },
  module: {
    rules: [
      {
        test: /\.jsx?/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
    ],
  },
};

module.exports = config;