import type { MetadataRoute } from 'next';
import { products } from '@/lib/data';

const SITE = 'https://ausgarden.intelliverse.tw';

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  const staticPages: MetadataRoute.Sitemap = [
    { url: `${SITE}/`,         lastModified: now, changeFrequency: 'weekly',  priority: 1.0 },
    { url: `${SITE}/courses/`, lastModified: now, changeFrequency: 'weekly',  priority: 0.9 },
    { url: `${SITE}/products/`,lastModified: now, changeFrequency: 'weekly',  priority: 0.9 },
    { url: `${SITE}/about/`,   lastModified: now, changeFrequency: 'monthly', priority: 0.7 },
    { url: `${SITE}/contact/`, lastModified: now, changeFrequency: 'monthly', priority: 0.6 },
  ];
  const productPages: MetadataRoute.Sitemap = products.map((p) => ({
    url: `${SITE}/products/${p.code}/`,
    lastModified: now,
    changeFrequency: 'monthly',
    priority: 0.7,
  }));
  return [...staticPages, ...productPages];
}
