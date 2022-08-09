module.exports = {
  publicPath: process.env.NODE_ENV === "production" ? "/app/" : "/",
  devServer: {
    proxy: "http://server:8000",
  },
};
