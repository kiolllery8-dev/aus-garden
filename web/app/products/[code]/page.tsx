import { notFound } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import Script from 'next/script';
import type { Metadata } from 'next';
import { products, displayName, priceNumber } from '@/lib/data';

const BP = process.env.NEXT_PUBLIC_BASE_PATH || '';
const SITE = 'https://ausgarden.intelliverse.tw';

export function generateStaticParams() {
  return products.map((p) => ({ code: p.code }));
}

export function generateMetadata({ params }: { params: { code: string } }): Metadata {
  const p = products.find((x) => x.code === params.code);
  if (!p) return { title: '商品不存在' };
  const name = displayName(p);
  const desc =
    [p.benefits, p.usp, p.ingredients].filter(Boolean).join(' ｜ ').slice(0, 150) ||
    `AUS GARDEN 澳維花園 ${name}，由芳療師親手調配的天然精油香氛商品。`;
  return {
    title: `${name}`,
    description: desc,
    keywords: [
      name, p.code, p.series || '', 'AUS GARDEN', '澳維花園', '精油', '香氛',
    ].filter(Boolean) as string[],
    alternates: { canonical: `/products/${p.code}/` },
    openGraph: {
      title: `${name}｜AUS GARDEN 澳維花園`,
      description: desc,
      images: p.image ? [{ url: `/${p.image}`, width: 720, height: 720, alt: name }] : [],
      type: 'article',
    },
    twitter: {
      card: 'summary_large_image',
      title: `${name}｜AUS GARDEN 澳維花園`,
      description: desc,
      images: p.image ? [`/${p.image}`] : [],
    },
  };
}

export default function ProductPage({ params }: { params: { code: string } }) {
  const p = products.find((x) => x.code === params.code);
  if (!p) notFound();
  const name = displayName(p);
  const price = priceNumber(p);

  // Product + Breadcrumb JSON-LD
  const ld = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Product',
        '@id': `${SITE}/products/${p.code}/#product`,
        name,
        sku: p.code,
        image: p.image ? `${SITE}/${p.image}` : undefined,
        description: [p.benefits, p.usp, p.ingredients].filter(Boolean).join(' ｜ '),
        brand: { '@type': 'Brand', name: 'AUS GARDEN 澳維花園' },
        category: p.series || p.category,
        ...(price
          ? {
              offers: {
                '@type': 'Offer',
                priceCurrency: 'TWD',
                price: price,
                availability: 'https://schema.org/InStock',
                seller: { '@type': 'Organization', name: 'AUS GARDEN 澳維花園' },
              },
            }
          : {}),
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: '首頁', item: `${SITE}/` },
          { '@type': 'ListItem', position: 2, name: '香氛商品', item: `${SITE}/products/` },
          { '@type': 'ListItem', position: 3, name, item: `${SITE}/products/${p.code}/` },
        ],
      },
    ],
  };

  return (
    <>
      <Script
        id={`ld-product-${p.code}`}
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(ld) }}
      />

      <section className="bg-sand/60">
        <div className="container py-10 text-xs text-ink/60">
          <nav aria-label="breadcrumb">
            <Link href="/" className="hover:text-forest">首頁</Link>
            <span className="mx-2">/</span>
            <Link href="/products" className="hover:text-forest">香氛商品</Link>
            <span className="mx-2">/</span>
            <span className="text-forest">{name}</span>
          </nav>
        </div>
      </section>

      <section className="container py-12 grid md:grid-cols-2 gap-12">
        <div className="relative aspect-square rounded-3xl overflow-hidden bg-gradient-to-br from-sand/60 via-cream to-cream border hairline">
          {p.image && (
            <Image
              src={`${BP}/${p.image}`}
              alt={name}
              fill
              sizes="(max-width:768px) 100vw, 50vw"
              className="object-contain p-8"
              priority
            />
          )}
        </div>
        <div>
          <p className="text-[11px] tracking-[0.3em] text-clay">{p.code} · {p.series || p.category}</p>
          <h1 className="mt-3 text-3xl md:text-4xl text-forest leading-tight">{name}</h1>
          <p className="mt-4 text-xl text-moss">
            {price ? `NT$ ${price.toLocaleString()}` : '價格洽詢'}
          </p>

          <div className="mt-8 space-y-6 text-sm leading-7">
            {p.benefits && (
              <div>
                <h2 className="text-base text-forest font-semibold mb-2">主要功效</h2>
                <p className="text-ink/80">{p.benefits}</p>
              </div>
            )}
            {p.audience && (
              <div>
                <h2 className="text-base text-forest font-semibold mb-2">適用對象</h2>
                <p className="text-ink/80">{p.audience}</p>
              </div>
            )}
            {p.ingredients && (
              <div>
                <h2 className="text-base text-forest font-semibold mb-2">主要成分</h2>
                <p className="text-ink/80">{p.ingredients}</p>
              </div>
            )}
            {p.usage && (
              <div>
                <h2 className="text-base text-forest font-semibold mb-2">使用方式</h2>
                <p className="text-ink/80">{p.usage}</p>
              </div>
            )}
            {p.usp && (
              <div>
                <h2 className="text-base text-forest font-semibold mb-2">品牌獨特賣點</h2>
                <p className="text-ink/80">{p.usp}</p>
              </div>
            )}
            {p.notes && (
              <div>
                <h2 className="text-base text-forest font-semibold mb-2">注意事項</h2>
                <p className="text-ink/70 text-xs">{p.notes}</p>
              </div>
            )}
          </div>

          <div className="mt-10 flex gap-3">
            <a href="https://line.me/R/ti/p/@auslife" className="btn btn-primary">LINE 詢問</a>
            <Link href="/products" className="btn btn-ghost">返回商品列表</Link>
          </div>
        </div>
      </section>

      {/* Related products */}
      <section className="container pb-20">
        <h2 className="text-2xl text-forest mb-6">同系列商品</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {products
            .filter((x) => x.code !== p.code && x.category === p.category)
            .slice(0, 4)
            .map((rp) => (
              <Link key={rp.code} href={`/products/${rp.code}`} className="group">
                <div className="relative aspect-square rounded-2xl bg-gradient-to-br from-sand/60 via-cream to-cream border hairline overflow-hidden">
                  {rp.image && (
                    <Image
                      src={`${BP}/${rp.image}`}
                      alt={displayName(rp)}
                      fill
                      sizes="25vw"
                      className="object-contain p-4 group-hover:scale-105 transition"
                    />
                  )}
                </div>
                <p className="mt-3 text-sm text-forest line-clamp-2">{displayName(rp)}</p>
              </Link>
            ))}
        </div>
      </section>
    </>
  );
}
