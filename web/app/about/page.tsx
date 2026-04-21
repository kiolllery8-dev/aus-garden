import Image from 'next/image';
const BP = process.env.NEXT_PUBLIC_BASE_PATH || '';

export const metadata = { title: '品牌故事｜AUS GARDEN 澳維花園' };

export default function AboutPage() {
  return (
    <>
      <section className="bg-sand/60">
        <div className="container py-20">
          <p className="text-xs tracking-[0.4em] text-moss mb-4">BRAND STORY</p>
          <h1 className="text-4xl md:text-5xl text-forest">從一座花園，<br />走進你的日常</h1>
        </div>
      </section>

      <section className="container py-16 grid md:grid-cols-2 gap-12 items-start">
        <div className="relative aspect-[4/5] rounded-3xl overflow-hidden bg-sand">
          <Image src={`${BP}/hero/hero.jpg`} alt="AUS GARDEN" fill sizes="(max-width:768px) 100vw, 50vw" className="object-cover" />
        </div>
        <div className="space-y-6 text-ink/80 leading-8">
          <p>
            AUS GARDEN 澳維花園，從一座充滿植物與香氣的小花園出發。
            我們相信，香氣是最直接的情緒語言——能喚起記憶、安撫情緒，也能標記一段重要時刻。
          </p>
          <p>
            我們透過三條路徑，把植物與香氣帶進你的生活：
            一是 <span className="text-forest font-medium">香氛體驗工作坊</span>，
            讓你用雙手做一件屬於自己的作品；
            二是 <span className="text-forest font-medium">精油香氛商品</span>，
            由芳療師親手調配，將手作品質帶回家；
            三是 <span className="text-forest font-medium">企業氣味藝術合作</span>，
            為品牌活動與團隊打造獨一無二的氣味記憶點。
          </p>
          <p>
            此外，我們也將 25 年品牌創業輔導經驗化為第四支柱——
            <span className="text-forest font-medium">創業輔導暨商業模式諮詢</span>，
            陪伴身心靈、香氛與手作創業者從零到一，建立自己的品牌系統。
          </p>
        </div>
      </section>

      <section className="bg-forest text-cream">
        <div className="container py-16">
          <h2 className="text-3xl">品牌主張</h2>
          <blockquote className="mt-8 text-xl md:text-2xl leading-relaxed text-sand max-w-3xl font-serif">
            「用雙手創作，用鼻子感受，
            每一個香氛作品，都是你與植物之間最美的對話。
            AUS GARDEN——讓生活從此充滿好聞的味道。」
          </blockquote>
        </div>
      </section>

      <section className="container py-16 grid md:grid-cols-4 gap-6">
        {[
          { n: '25+', t: '年品牌創業輔導經驗' },
          { n: '9+', t: '類手作課程系列' },
          { n: '100%', t: '天然精油與植物原料' },
          { n: '∞', t: '氣味與記憶的組合' },
        ].map((x) => (
          <div key={x.t} className="text-center p-8 rounded-2xl bg-white/70 border hairline">
            <div className="text-4xl font-serif text-forest">{x.n}</div>
            <div className="mt-3 text-sm text-ink/70">{x.t}</div>
          </div>
        ))}
      </section>
    </>
  );
}
