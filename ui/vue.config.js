module.exports = {
	css: {
        loaderOptions: {
            less: {
                javascriptEnabled: true
            }
        }
    },
    publicPath: process.env.NODE_ENV === 'production' ?
        '/' : '/', // wa: nlu
    devServer: {
        proxy: {
            '/api': {
                target: 'http://10.25.9.37:8899/api/',
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            },
        }
    }
}
