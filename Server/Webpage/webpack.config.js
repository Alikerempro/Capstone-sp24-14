const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: {
    main: path.join(__dirname, "src", "index.js"),
    settings: path.join(__dirname, "src", "settings.js")
  },
  output: {
    path:path.resolve(__dirname, "dist"),
    filename:"[name].js"
  },
  module: {
    rules: [
      {
        test: /\.?js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      filename: "index.html",
      template: path.join(__dirname, "src", "index.html"),
      chunks: ['main']
    }),
    new HtmlWebpackPlugin({
      filename: "settings.html",
      template: path.join(__dirname, "src", "settings.html"),
      chunks: ['settings']
    }),
  ],
}