/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/check_session',
        destination: 'https://maestro-web-backend-68382569913.us-east4.run.app/check_session',
      },
      {
        source: '/api/:path*',
        destination: 'https://maestro-web-backend-68382569913.us-east4.run.app/:path*',
      },
      {
        source: '/static/:path*',
        destination: 'https://maestro-web-backend-68382569913.us-east4.run.app/static/:path*',
      }
    ];
  }
};
module.exports = nextConfig;
