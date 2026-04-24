import type { Metadata } from 'next';
import Script from 'next/script';
import { products, displayName, priceNumber } from '@/lib/data';

const SITE = 'https://ausgarden.intelliverse.tw';

export const metadata: Metadata = {
  title: '香氛商品｜精油・擴香・滾珠・按摩油・臉部保養｜AUS GARDEN 澳維花園',
  description:
    'AUS GARDEN 澳維花園 80+ 款手工調配香氛商品：天然精油、居家擴香、隨身滾珠、按摩精油、基底油、護膚油、純露花水、臉部保養。芳療師親手調配，100% 天然植物原料。',
  keywords: [
    '精油', '擴香', '滾珠精油', '按摩精油', '基底油', '護膚油',
    '玫瑰純露', '荷荷芭油', '薰衣草精油', '尤加利精油', '茶樹精油',
    'AUS GARDEN', '澳維花園', '天然香氛商品', '芳療商品',
  ],
  alternates: { canonical: '/products/' },
  openGraph: {
    title: '香氛商品｜AUS GARDEN 澳維花園',
    description: '80+ 款手工調配精油香氛商品。',
    images: ['/hero/hero.jpg'],
  },
};

export default function ProductsLayout({ children }: { children: React.ReactNode }) {
  // ItemList of all products for rich snippets
  const itemList = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: 'AUS GARDEN 澳維花園 香氛商品',
    numberOfItems: products.length,
    itemListElement: products.map((p, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      url: `${SITE}/products/${p.code}/`,
      name: displayName(p),
      ...(p.image ? { image: `${SITE}/${p.image}` } : {}),
      ...(priceNumber(p)
        ? { offers: { '@type': 'Offer', price: priceNumber(p), priceCurrency: 'TWD' } }
        : {}),
    })),
  };
  const bread = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: '首頁', item: `${SITE}/` },
      { '@type': 'ListItem', position: 2, name: '香氛商品', item: `${SITE}/products/` },
    ],
  };
  return (
    <>
      <Script id="ld-products-list" type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(itemList) }} />
      <Script id="ld-products-bc" type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(bread) }} />
      {children}
    </>
  );
}
