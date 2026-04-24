import Link from 'next/link';
import Image from 'next/image';
import { courses } from '@/lib/data';

const BP = process.env.NEXT_PUBLIC_BASE_PATH || '';

import Script from 'next/script';
import type { Metadata } from 'next';

const SITE = 'https://ausgarden.intelliverse.tw';

export const metadata: Metadata = {
  title: '手作香氛課程｜蠟燭 DIY・精油調香・冷製皂・沐浴球｜台中太平',
  description:
    'AUS GARDEN 澳維花園 9 大手作香氛體驗工作坊：容器蠟燭、大豆蠟進階、個人香水調製、居家擴香、天然護膚油、開運香氣水晶香水、香氛沐浴球、冷製手工皂、固體香膏。台中太平實體課程，1.5–3 小時完成。企業 Team Building、婚禮派對、品牌活動客製。',
  keywords: [
    '手作課程', '香氛工作坊', '調香工作坊', '蠟燭 DIY', '精油課程',
    '冷製皂課程', '手工皂課程', '沐浴球手作', '固體香水', '個人香水',
    '台中手作', '太平手作', 'Team Building', '婚禮小物 DIY', '香氛體驗',
    'AUS GARDEN', '澳維花園',
  ],
  alternates: { canonical: '/courses/' },
  openGraph: {
    title: '手作香氛課程｜AUS GARDEN 澳維花園',
    description: '9 大香氛體驗手作工作坊，台中太平實體課程。',
    images: ['/courses/personal-perfume.jpg'],
  },
};

const categories = [
  { key: 'A', label: 'A · 蠟燭系列' },
  { key: 'B', label: 'B · 精油調香' },
  { key: 'C', label: 'C · 生活手作' },
];

const SITE_URL = 'https://ausgarden.intelliverse.tw';

export default function CoursesPage() {
  const courseLd = {
    '@context': 'https://schema.org',
    '@graph': courses.map((c) => ({
      '@type': 'Course',
      name: c.title,
      description: c.desc,
      provider: { '@type': 'Organization', name: 'AUS GARDEN 澳維花園', sameAs: SITE_URL },
      offers: {
        '@type': 'Offer',
        price: c.priceFrom,
        priceCurrency: 'TWD',
        availability: 'https://schema.org/InStock',
      },
      hasCourseInstance: {
        '@type': 'CourseInstance',
        courseMode: 'onsite',
        duration: c.duration,
        location: {
          '@type': 'Place',
          name: 'AUS GARDEN 澳維花園工作坊',
          address: '台中市太平區精美路 122 號',
        },
      },
    })),
  };
  const breadLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: '首頁', item: `${SITE_URL}/` },
      { '@type': 'ListItem', position: 2, name: '手作課程', item: `${SITE_URL}/courses/` },
    ],
  };
  return (
    <>
      <Script id="ld-courses" type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(courseLd) }} />
      <Script id="ld-courses-bc" type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadLd) }} />
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
