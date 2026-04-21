import type { Metadata } from 'next';
import './globals.css';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: 'AUS GARDEN 澳維花園｜From the Garden, Into Your Life',
  description:
    '植物之力，生活之美。AUS GARDEN 澳維花園提供香氛體驗工作坊、精油香氛商品與企業氣味藝術合作。',
  keywords: ['AUS GARDEN', '澳維花園', '香氛', '精油', '蠟燭手作', '調香工作坊', '台中手作課程'],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-Hant">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Noto+Serif+TC:wght@400;500;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-cream text-ink">
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
