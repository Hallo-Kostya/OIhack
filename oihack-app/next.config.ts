import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  experimental: {
    appDir: true, // Включить App Router
  },
};

module.exports = nextConfig

export default nextConfig;
