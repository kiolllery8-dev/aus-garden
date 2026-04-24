import type { MetadataRoute } from 'next';

const SITE = 'https://ausgarden.intelliverse.tw';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: '*', allow: '/' }],
    sitemap: `${SITE}/sitemap.xml`,
    host: SITE,
  };
}
