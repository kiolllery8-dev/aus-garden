import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: '聯絡我們｜預約課程・企業合作｜AUS GARDEN 澳維花園',
  description:
    'AUS GARDEN 澳維花園聯絡資訊｜台中市太平區精美路 122 號 ｜客服 04-2275-2009 ｜LINE @auslife ｜信箱 salesgoldfishion@gmail.com ｜預約手作課程、企業 Team Building 客製、婚禮派對、商品禮盒詢問。',
  keywords: [
    '聯絡 AUS GARDEN', '預約課程', '企業合作', '台中香氛', 'LINE auslife',
    '太平香氛工作坊', '婚禮小物客製', 'Team Building',
  ],
  alternates: { canonical: '/contact/' },
  openGraph: {
    title: '聯絡我們｜AUS GARDEN 澳維花園',
    description: '預約課程・企業洽詢・LINE @auslife',
    images: ['/hero/hero.jpg'],
  },
};

export default function ContactPage() {
  return (
    <>
      <section className="bg-sand/60">
        <div className="container py-20">
          <p className="text-xs tracking-[0.4em] text-moss mb-4">CONTACT</p>
          <h1 className="text-4xl md:text-5xl text-forest">預約課程・企業洽詢</h1>
          <p className="mt-6 max-w-2xl text-ink/75 leading-8">
            無論是個人手作課程預約、企業 Team Building、婚禮派對客製，或創業輔導諮詢，
            都歡迎透過下方管道與我們聯絡。
          </p>
        </div>
      </section>

      <section className="container py-16 grid md:grid-cols-2 gap-12">
        <div className="space-y-6">
          <div className="p-6 rounded-2xl bg-white/70 border hairline">
            <h3 className="text-lg text-forest">工作坊地址</h3>
            <p className="mt-2 text-ink/80">台中市太平區精美路 122 號</p>
          </div>
          <div className="p-6 rounded-2xl bg-white/70 border hairline">
            <h3 className="text-lg text-forest">客服電話</h3>
            <a href="tel:0422752009" className="mt-2 block text-ink/80">04-2275-2009</a>
          </div>
          <div className="p-6 rounded-2xl bg-white/70 border hairline">
            <h3 className="text-lg text-forest">客服信箱</h3>
            <a href="mailto:salesgoldfishion@gmail.com" className="mt-2 block text-ink/80">
              salesgoldfishion@gmail.com
            </a>
          </div>
          <div className="p-6 rounded-2xl bg-white/70 border hairline">
            <h3 className="text-lg text-forest">LINE 官方帳號</h3>
            <a href="https://line.me/R/ti/p/@auslife" className="mt-2 block text-ink/80">@auslife</a>
          </div>
          <div className="p-6 rounded-2xl bg-white/70 border hairline">
            <h3 className="text-lg text-forest">客服時段</h3>
            <p className="mt-2 text-ink/80">週一至週五 10:00–18:00</p>
          </div>
        </div>

        <form
          className="p-8 rounded-2xl bg-white/80 border hairline space-y-5"
          action="mailto:salesgoldfishion@gmail.com"
          method="post"
          encType="text/plain"
        >
          <h2 className="text-2xl text-forest">線上詢問</h2>
          <div>
            <label className="block text-sm text-ink/70 mb-1">姓名</label>
            <input name="name" required className="w-full rounded-lg border hairline bg-cream/60 px-4 py-3 focus:outline-none focus:border-forest" />
          </div>
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-ink/70 mb-1">電話</label>
              <input name="phone" className="w-full rounded-lg border hairline bg-cream/60 px-4 py-3 focus:outline-none focus:border-forest" />
            </div>
            <div>
              <label className="block text-sm text-ink/70 mb-1">Email</label>
              <input name="email" type="email" required className="w-full rounded-lg border hairline bg-cream/60 px-4 py-3 focus:outline-none focus:border-forest" />
            </div>
          </div>
          <div>
            <label className="block text-sm text-ink/70 mb-1">詢問類型</label>
            <select name="topic" className="w-full rounded-lg border hairline bg-cream/60 px-4 py-3 focus:outline-none focus:border-forest">
              <option>個人課程預約</option>
              <option>企業 / 團體客製</option>
              <option>商品 / 禮盒詢問</option>
              <option>創業輔導諮詢</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-ink/70 mb-1">留言</label>
            <textarea name="message" rows={5} className="w-full rounded-lg border hairline bg-cream/60 px-4 py-3 focus:outline-none focus:border-forest" />
          </div>
          <button type="submit" className="btn btn-primary w-full">送出詢問</button>
          <p className="text-xs text-ink/50">
            送出後將開啟您的郵件軟體，也歡迎直接透過 LINE @auslife 與我們聯絡。
          </p>
        </form>
      </section>
    </>
  );
}
