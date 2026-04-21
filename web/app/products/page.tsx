import { products } from '@/lib/data';

export const metadata = { title: '香氛商品｜AUS GARDEN 澳維花園' };

export default function ProductsPage() {
  return (
    <>
      <section className="bg-sand/60">
        <div className="container py-20">
          <p className="text-xs tracking-[0.4em] text-moss mb-4">SHOP</p>
          <h1 className="text-4xl md:text-5xl text-forest">精油香氛商品</h1>
          <p className="mt-6 max-w-2xl text-ink/75 leading-8">
            由芳療師親手調配的簽名系列。
            選用天然精油與植物原料，為日常生活帶來植物香氣的療癒節奏。
          </p>
        </div>
      </section>

      <section className="container py-16">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {products.map((p) => (
            <article key={p.slug} className="group">
              <div className={`relative aspect-square rounded-2xl bg-gradient-to-br ${p.cover} overflow-hidden`}>
                {p.tag && (
                  <span className="absolute top-4 left-4 text-[11px] tracking-widest bg-forest text-cream px-3 py-1 rounded-full">
                    {p.tag}
                  </span>
                )}
              </div>
              <div className="mt-4">
                <h3 className="text-lg text-forest">{p.name}</h3>
                <p className="text-xs text-ink/60 mt-1">{p.subtitle}</p>
                <div className="mt-3 flex items-center justify-between">
                  <span className="text-sm text-moss">NT$ {p.price.toLocaleString()}</span>
                  <a href="https://line.me/R/ti/p/@auslife" className="text-xs tracking-widest text-forest group-hover:underline">
                    詢問 →
                  </a>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="container pb-20">
        <div className="rounded-3xl bg-white/70 border hairline p-10 text-center">
          <h2 className="text-2xl text-forest">禮盒客製、企業送禮</h2>
          <p className="mt-4 text-ink/75">可依品牌調性客製包裝、刻字與香調搭配。歡迎透過 LINE 洽詢。</p>
          <a href="https://line.me/R/ti/p/@auslife" className="mt-6 inline-flex btn btn-primary">LINE 聯絡 @auslife</a>
        </div>
      </section>
    </>
  );
}
