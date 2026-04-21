'use client';
import { useMemo, useState } from 'react';
import Image from 'next/image';
import { products, displayName, priceNumber, productCategories } from '@/lib/data';

const BP = process.env.NEXT_PUBLIC_BASE_PATH || '';

export default function ProductsPage() {
  const [cat, setCat] = useState<string>('全部');
  const [q, setQ] = useState('');

  const list = useMemo(() => {
    return products.filter((p) => {
      if (cat !== '全部' && p.category !== cat) return false;
      if (q && !displayName(p).toLowerCase().includes(q.toLowerCase())) return false;
      return true;
    });
  }, [cat, q]);

  return (
    <>
      <section className="bg-sand/60">
        <div className="container py-20">
          <p className="text-xs tracking-[0.4em] text-moss mb-4">SHOP</p>
          <h1 className="text-4xl md:text-5xl text-forest">精油香氛商品</h1>
          <p className="mt-6 max-w-2xl text-ink/75 leading-8">
            AUS GARDEN 澳維花園 由芳療師親手調配的完整商品系列——
            精油、按摩油、滾珠、純露與臉部保養。全線採用天然植物原料，為日常生活帶來植物香氣的療癒節奏。
          </p>
        </div>
      </section>

      {/* Filters */}
      <section className="container pt-10">
        <div className="flex flex-col md:flex-row gap-4 md:items-center md:justify-between">
          <div className="flex flex-wrap gap-2">
            {productCategories.map((c) => (
              <button
                key={c}
                onClick={() => setCat(c)}
                className={`px-4 py-2 rounded-full text-sm border hairline transition ${
                  cat === c ? 'bg-forest text-cream border-forest' : 'bg-white/60 text-forest hover:bg-white'
                }`}
              >
                {c}
              </button>
            ))}
          </div>
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="搜尋商品名稱…"
            className="w-full md:w-72 px-4 py-2 rounded-full bg-white/60 border hairline text-sm focus:outline-none focus:border-forest"
          />
        </div>
        <p className="mt-4 text-xs text-ink/60">共 {list.length} 件商品</p>
      </section>

      <section className="container py-10 pb-20">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {list.map((p) => {
            const price = priceNumber(p);
            const name = displayName(p);
            return (
              <article key={p.code} className="group bg-white rounded-2xl overflow-hidden border hairline hover:shadow-lg transition">
                <div className="relative aspect-square bg-gradient-to-br from-sand/60 via-cream to-cream">
                  {p.image ? (
                    <Image
                      src={`${BP}/${p.image}`}
                      alt={name}
                      fill
                      sizes="(max-width: 768px) 50vw, 25vw"
                      className="object-contain p-4 group-hover:scale-105 transition duration-500"
                    />
                  ) : (
                    <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-sand to-moss/20 text-forest text-xs tracking-widest">
                      AUS GARDEN
                    </div>
                  )}
                </div>
                <div className="p-4">
                  <p className="text-[10px] tracking-widest text-clay">{p.code}</p>
                  <h3 className="mt-1 text-sm md:text-base text-forest leading-tight line-clamp-2 min-h-[2.75em]">
                    {name}
                  </h3>
                  <div className="mt-3 flex items-center justify-between">
                    <span className="text-sm text-moss">
                      {price ? `NT$ ${price.toLocaleString()}` : '洽詢'}
                    </span>
                    <a
                      href="https://line.me/R/ti/p/@auslife"
                      className="text-[11px] tracking-widest text-forest hover:underline"
                    >
                      詢問 →
                    </a>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
        {list.length === 0 && (
          <p className="text-center py-20 text-ink/50">找不到符合條件的商品</p>
        )}
      </section>

      <section className="container pb-20">
        <div className="rounded-3xl bg-forest text-cream p-10 text-center">
          <h2 className="text-2xl">禮盒客製、企業送禮</h2>
          <p className="mt-4 text-sand/90">可依品牌調性客製包裝、刻字與香調搭配。歡迎透過 LINE 洽詢。</p>
          <a href="https://line.me/R/ti/p/@auslife" className="mt-6 inline-flex btn bg-cream text-forest hover:bg-sand">
            LINE 聯絡 @auslife
          </a>
        </div>
      </section>
    </>
  );
}
