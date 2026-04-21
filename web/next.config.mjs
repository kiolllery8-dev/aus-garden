/**
 * Next.js config for GitHub Pages static export.
 * If your repo is "aus-garden", set NEXT_PUBLIC_BASE_PATH=/aus-garden at build time.
 * For custom domain (CNAME), leave NEXT_PUBLIC_BASE_PATH empty.
 */
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || '';

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: { unoptimized: true },
  trailingSlash: true,
  basePath,
  assetPrefix: basePath || undefined,
  env: {
    NEXT_PUBLIC_BASE_PATH: basePath,
  },
};

export default nextConfig;
