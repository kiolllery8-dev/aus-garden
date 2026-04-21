import Link from 'next/link';
import { courses, products } from '@/lib/data';

export default function HomePage() {
  const featuredCourses = courses.slice(0, 4);
  const featuredProducts = products.slice(0, 4);

  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-sand via-cream to-moss/20" aria-hidden />
        <div className="container relative py-24 md:py-36 grid md:grid-cols-2 gap-12 items-center">
          <div>
            <p className="text-xs tracking-[0.4em] text-moss mb-6">FROM THE GARDEN, INTO YOUR LIFE</p>
            <h1 className="text-4xl md:text-6xl leading-tight text-forest">
              植物之力<br />生活之美
            </h1>
            <p className="mt-8 text-base md:text-lg leading-8 text-ink/80 max-w-lg">
              用雙手創作，用鼻子感受。每一個香氛作品，都是你與植物之間最美的對話。
              AUS GARDEN 澳維花園——讓生活從此充滿好聞的味道。
            </p>
            <div className="mt-10 flex gap-4">
              <Link href="/courses" className="btn btn-primary">預約手作課程</Link>
              <Link href="/products" className="btn btn-ghost">探索香氛商品</Link>
            </div>
          </div>
          <div className="relative aspect-[4/5] rounded-3xl bg-gradient-to-br from-moss/30 via-sand to-clay/40 shadow-xl overflow-hidden">
            <div className="absolute inset-0 flex items-end p-8 text-cream">
              <div className="bg-forest/70 backdrop-blur rounded-2xl px-5 py-4">
                <p className="text-xs tracking-widest text-sand">SIGNATURE SERIES</p>
                <p className="text-lg mt-1">森林書房・手工香氛</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Three Pillars */}
      <section className="container py-20">
        <div className="flex items-end justify-between mb-12">
          <div>
            <p className="text-xs tracking-[0.4em] text-moss mb-3">OUR PILLARS</p>
            <h2 className="text-3xl md:text-4xl text-forest">品牌三支柱</h2>
          </div>
          <Link href="/about" className="text-sm text-moss hover:underline">了解更多 →</Link>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { t: '香氛體驗工作坊', d: '從蠟燭、香水到冷製皂，九大手作系列陪你從生活中長出儀式感。', n: '01' },
            { t: '精油香氛商品', d: '由芳療師親手調配的簽名系列，蠟燭、擴香、滾珠與護膚油。', n: '02' },
            { t: '企業氣味藝術合作', d: 'Team Building、婚禮派對、品牌開幕，客製專屬氣味記憶點。', n: '03' },
          ].map((x) => (
            <div key={x.n} className="p-8 rounded-2xl bg-white/60 border hairline hover:bg-white transition">
              <div className="text-xs tracking-[0.3em] text-clay">{x.n}</div>
              <h3 className="mt-3 text-2xl text-forest">{x.t}</h3>
              <p className="mt-4 text-sm leading-7 text-ink/75">{x.d}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Featured Courses */}
      <section className="bg-sand/60 py-20">
        <div className="container">
          <div className="flex items-end justify-between mb-12">
            <div>
              <p className="text-xs tracking-[0.4em] text-moss mb-3">WORKSHOP</p>
              <h2 className="text-3xl md:text-4xl text-forest">精選手作課程</h2>
            </div>
            <Link href="/courses" className="text-sm text-moss hover:underline">全部課程 →</Link>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredCourses.map((c) => (
              <article key={c.slug} className="group bg-cream rounded-2xl overflow-hidden border hairline">
                <div className={`aspect-[4/5] bg-gradient-to-br ${c.cover} flex items-end p-4`}>
                  <span className="text-[11px] tracking-widest bg-cream/90 text-forest px-3 py-1 rounded-full">
                    {c.category}
                  </span>
                </div>
                <div className="p-5">
                  <h3 className="text-lg text-forest leading-tight">{c.title}</h3>
                  <p className="mt-2 text-xs text-ink/60">{c.duration}</p>
                  <p className="mt-3 text-sm leading-6 text-ink/75 line-clamp-2">{c.desc}</p>
                  <div className="mt-5 flex items-center justify-between">
                    <span className="text-sm text-moss">NT$ {c.priceFrom.toLocaleString()} 起</span>
                    <Link href="/contact" className="text-xs tracking-widest text-forest group-hover:underline">預約 →</Link>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="container py-20">
        <div className="flex items-end justify-between mb-12">
          <div>
            <p className="text-xs tracking-[0.4em] text-moss mb-3">SHOP</p>
            <h2 className="text-3xl md:text-4xl text-forest">香氛商品</h2>
          </div>
          <Link href="/products" className="text-sm text-moss hover:underline">所有商品 →</Link>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {featuredProducts.map((p) => (
            <article key={p.slug} className="group">
              <div className={`relative aspect-square rounded-2xl bg-gradient-to-br ${p.cover} overflow-hidden`}>
                {p.tag && (
                  <span className="absolute top-4 left-4 text-[11px] tracking-widest bg-forest text-cream px-3 py-1 rounded-full">
                    {p.tag}
                  </span>
                )}
              </div>
              <div className="mt-4">
                <h3 className="text-base text-forest">{p.name}</h3>
                <p className="text-xs text-ink/60 mt-1">{p.subtitle}</p>
                <p className="text-sm text-moss mt-2">NT$ {p.price.toLocaleString()}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* Brand Story Teaser */}
      <section className="bg-forest text-cream">
        <div className="container py-20 grid md:grid-cols-2 gap-12 items-center">
          <div className="aspect-[5/4] rounded-3xl bg-gradient-to-br from-moss to-clay/70" />
          <div>
            <p className="text-xs tracking-[0.4em] text-sand mb-4">BRAND STORY</p>
            <h2 className="text-3xl md:text-4xl">從一座花園，走進你的日常</h2>
            <p className="mt-6 leading-8 text-sand/90">
              AUS GARDEN 澳維花園相信，香氣是最直接的情緒語言。
              我們從植物出發，透過手作課程與香氛商品，把屬於你的氣味記憶帶回日常生活裡。
            </p>
            <Link href="/about" className="mt-8 inline-flex btn bg-cream text-forest hover:bg-sand">
              了解品牌故事
            </Link>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="container py-20 text-center">
        <p className="text-xs tracking-[0.4em] text-moss mb-4">VISIT US</p>
        <h2 className="text-3xl md:text-4xl text-forest">歡迎走進澳維花園</h2>
        <p className="mt-5 text-ink/75">台中市太平區精美路 122 號 · 週一至週五 10:00–18:00</p>
        <div className="mt-8 flex justify-center gap-4">
          <Link href="/contact" className="btn btn-primary">預約課程 / 詢問企業合作</Link>
          <a href="https://line.me/R/ti/p/@auslife" className="btn btn-ghost">加入 LINE @auslife</a>
        </div>
      </section>
    </>
  );
}
