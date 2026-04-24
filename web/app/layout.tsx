import type { Metadata, Viewport } from 'next';
import Script from 'next/script';
import './globals.css';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

const SITE_URL = 'https://ausgarden.intelliverse.tw';

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: 'AUS GARDEN 澳維花園｜手作香氛工作坊・精油商品・企業氣味藝術｜台中太平',
    template: '%s｜AUS GARDEN 澳維花園',
  },
  description:
    'AUS GARDEN 澳維花園｜台中太平手作香氛體驗工作坊，提供蠟燭手作、精油調香、天然護膚油、冷製皂、沐浴球等 9 大手作課程，以及 80+ 款芳療師手工調配精油、擴香、滾珠、按摩油與臉部保養商品。企業 Team Building、婚禮派對、品牌活動客製氣味合作。From the Garden, Into Your Life.',
  keywords: [
    'AUS GARDEN', '澳維花園', '澳維', 'Aus Garden',
    '手作香氛', '香氛工作坊', '調香工作坊', '香氛課程',
    '精油', '精油商品', '天然精油', '薰衣草精油', '尤加利精油', '茶樹精油',
    '擴香', '擴香瓶', '滾珠精油', '按摩精油', '基底油',
    '蠟燭手作', '大豆蠟蠟燭', '香氛蠟燭',
    '冷製皂', '手工皂', '沐浴球', '固體香水',
    '護膚油', '玫瑰果油', '荷荷芭油', '臉部保養',
    '企業 Team Building', '婚禮小物', '品牌活動',
    '台中手作', '太平手作', '台中香氛課程', '台中精油',
    '芳療', '芳療師', '芳香療法',
  ],
  authors: [{ name: 'AUS GARDEN 澳維花園' }],
  creator: 'AUS GARDEN 澳維花園',
  publisher: 'AUS GARDEN 澳維花園',
  alternates: { canonical: '/' },
  openGraph: {
    type: 'website',
    locale: 'zh_TW',
    url: SITE_URL,
    siteName: 'AUS GARDEN 澳維花園',
    title: 'AUS GARDEN 澳維花園｜From the Garden, Into Your Life',
    description:
      '台中太平手作香氛工作坊 + 精油香氛商品 + 企業氣味藝術合作。9 大手作課程 · 80+ 款手工調配商品。',
    images: [
      { url: '/hero/hero.jpg', width: 1080, height: 1440, alt: 'AUS GARDEN 澳維花園 手作香氛' },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AUS GARDEN 澳維花園｜From the Garden, Into Your Life',
    description:
      '台中太平手作香氛工作坊 + 精油香氛商品 + 企業氣味藝術合作。',
    images: ['/hero/hero.jpg'],
  },
  robots: {
    index: true, follow: true,
    googleBot: { index: true, follow: true, 'max-image-preview': 'large', 'max-snippet': -1 },
  },
  category: 'Lifestyle · Aromatherapy · Handcraft Workshop',
  icons: { icon: '/favicon.ico' },
};

export const viewport: Viewport = {
  themeColor: '#3F4A2E',
  width: 'device-width',
  initialScale: 1,
};

// Site-wide structured data (Organization + LocalBusiness + WebSite)
const structuredData = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'Organization',
      '@id': `${SITE_URL}/#organization`,
      name: 'AUS GARDEN 澳維花園',
      alternateName: ['AUS GARDEN', '澳維花園', 'Aus Garden'],
      url: SITE_URL,
      logo: `${SITE_URL}/hero/hero.jpg`,
      image: `${SITE_URL}/hero/hero.jpg`,
      description: '台中太平手作香氛體驗工作坊、精油香氛商品、企業氣味藝術合作。',
      email: 'salesgoldfishion@gmail.com',
      telephone: '+886-4-2275-2009',
      sameAs: ['https://line.me/R/ti/p/@auslife'],
    },
    {
      '@type': 'LocalBusiness',
      '@id': `${SITE_URL}/#business`,
      name: 'AUS GARDEN 澳維花園',
      image: `${SITE_URL}/hero/hero.jpg`,
      url: SITE_URL,
      telephone: '+886-4-2275-2009',
      email: 'salesgoldfishion@gmail.com',
      priceRange: 'NT$ 500 – 5,000',
      address: {
        '@type': 'PostalAddress',
        streetAddress: '精美路 122 號',
        addressLocality: '太平區',
        addressRegion: '台中市',
        addressCountry: 'TW',
      },
      geo: { '@type': 'GeoCoordinates', latitude: 24.136, longitude: 120.717 },
      openingHoursSpecification: [
        {
          '@type': 'OpeningHoursSpecification',
          dayOfWeek: ['Monday','Tuesday','Wednesday','Thursday','Friday'],
          opens: '10:00', closes: '18:00',
        },
      ],
      hasOfferCatalog: {
        '@type': 'OfferCatalog',
        name: 'AUS GARDEN 手作課程與香氛商品',
      },
    },
    {
      '@type': 'WebSite',
      '@id': `${SITE_URL}/#website`,
      url: SITE_URL,
      name: 'AUS GARDEN 澳維花園',
      publisher: { '@id': `${SITE_URL}/#organization` },
      inLanguage: 'zh-Hant',
    },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-Hant">
      <head>
        <meta name="google-site-verification" content="eBQecTnxY_7xwmP5sqWgCnpTVLZg47BsjpWEtGVn-Uk" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Noto+Serif+TC:wght@400;500;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-cream text-ink">
        <Script
          id="ld-global"
          type="application/ld+json"
          strategy="beforeInteractive"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
