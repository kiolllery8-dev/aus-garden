import Link from 'next/link';
import Image from 'next/image';
import { courses } from '@/lib/data';

const BP = process.env.NEXT_PUBLIC_BASE_PATH || '';

export const metadata = { title: '手作課程｜AUS GARDEN 澳維花園' };

const categories = [
  { key: 'A', label: 'A · 蠟燭系列' },
  { key: 'B', label: 'B · 精油調香' },
  { key: 'C', label: 'C · 生活手作' },
];

export default function CoursesPage() {
  return (
    <>
      <section className="bg-sand/60">
        <div className="container py-20">
          <p className="text-xs tracking-[0.4em] text-moss mb-4">WORKSHOPS</p>
          <h1 className="text-4xl md:text-5xl text-forest">香氛體驗手作課程</h1>
          <p className="mt-6 max-w-2xl text-ink/75 leading-8">
            所有課程均為體驗型手作工作坊，由專業芳療師帶領，適合初學者到進階學員。
            課程不提供任何認證或證照，只提供一段專屬於你的植物與香氣時光。
          </p>
        </div>
      </section>

      {categories.map((cat) => {
        const list = courses.filter((c) => c.category.startsWith(cat.key));
        if (list.length === 0) return null;
        return (
          <section key={cat.key} className="container py-16">
            <h2 className="text-2xl md:text-3xl text-forest mb-8">{cat.label}</h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {list.map((c) => (
                <article key={c.slug} className="group bg-white rounded-2xl overflow-hidden border hairline hover:shadow-lg transition">
                  <div className="relative aspect-[4/3] overflow-hidden bg-sand">
                    <Image
                      src={`${BP}/courses/${c.slug}.jpg`}
                      alt={c.title}
                      fill
                      sizes="(max-width:768px) 100vw, 33vw"
                      className="object-cover group-hover:scale-105 transition duration-500"
                    />
                  </div>
                  <div className="p-6">
                    <h3 className="text-xl text-forest">{c.title}</h3>
                    <p className="mt-2 text-xs text-ink/60">{c.duration}</p>
                    <p className="mt-3 text-sm leading-6 text-ink/75">{c.desc}</p>
                    <div className="mt-6 flex items-center justify-between">
                      <span className="text-sm text-moss">NT$ {c.priceFrom.toLocaleString()} 起</span>
                      <Link href="/contact" className="text-xs tracking-widest text-forest hover:underline">
                        預約 →
                      </Link>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </section>
        );
      })}

      <section className="bg-forest text-cream">
        <div className="container py-16 grid md:grid-cols-2 gap-10 items-center">
          <div>
            <p className="text-xs tracking-[0.4em] text-sand mb-3">CORPORATE</p>
            <h2 className="text-3xl">D 類｜企業客製工作坊</h2>
            <p className="mt-5 leading-8 text-sand/90">
              Team Building、婚禮派對、品牌活動、門市開幕。
              提供 10–100 人客製化香氛手作體驗，可依主題調整香調、包裝與品牌 Logo。
            </p>
          </div>
          <div>
            <Link href="/contact" className="btn bg-cream text-forest hover:bg-sand">洽詢企業合作</Link>
          </div>
        </div>
      </section>
    </>
  );
}
