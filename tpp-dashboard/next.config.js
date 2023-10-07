const withWorkers = require('@zeit/next-workers');

module.exports = withWorkers({
  experimental: { esmExternals: 'loose' },
  webpack: (config) => {
    config.module.rules.push({
      test: /\.worker\.js$/,
      use: { loader: 'worker-loader' },
    });

    return config;
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:5002/api/:path*',
      },
    ];
  },
});
