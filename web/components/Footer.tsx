import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="mt-24 bg-forest text-cream">
      <div className="container py-16 grid md:grid-cols-4 gap-10">
        <div>
          <div className="font-serif text-2xl tracking-widest">AUS GARDEN</div>
          <div className="text-xs tracking-[0.3em] mt-1 text-sand">澳維花園</div>
          <p className="mt-6 text-sm leading-7 text-sand/90">
            From the Garden, Into Your Life.
            <br />
            植物之力，生活之美。
          </p>
        </div>

        <div>
          <h4 className="text-sm tracking-widest mb-4">服務項目</h4>
          <ul className="space-y-2 text-sm text-sand/90">
            <li><Link href="/courses">香氛體驗工作坊</Link></li>
            <li><Link href="/products">精油香氛商品</Link></li>
            <li><Link href="/contact">企業合作 / Team Building</Link></li>
            <li><Link href="/contact">創業輔導諮詢</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-sm tracking-widest mb-4">聯絡資訊</h4>
          <ul className="space-y-2 text-sm text-sand/90">
            <li>台中市太平區精美路 122 號</li>
            <li>客服電話：04-2275-2009</li>
            <li>信箱：salesgoldfishion@gmail.com</li>
            <li>LINE：@auslife</li>
            <li>週一至週五 10:00–18:00</li>
          </ul>
        </div>

        <div>
          <h4 className="text-sm tracking-widest mb-4">關注我們</h4>
          <ul className="space-y-2 text-sm text-sand/90">
            <li><a href="#" rel="noopener">Instagram</a></li>
            <li><a href="#" rel="noopener">Facebook</a></li>
            <li><a href="#" rel="noopener">LINE 官方帳號</a></li>
          </ul>
        </div>
      </div>
      <div className="border-t border-cream/10">
        <div className="container py-6 text-xs text-sand/70 flex flex-col md:flex-row justify-between gap-2">
          <span>© {new Date().getFullYear()} AUS GARDEN 澳維花園. All rights reserved.</span>
          <span>Handcrafted with plants & scent.</span>
        </div>
      </div>
      <div className="border-t border-cream/10 bg-forest/95">
        <div className="container py-4 text-center text-xs text-sand/80">
          網頁設計 by{' '}
          <a
            href="https://show.intelliverse.tw"
            target="_blank"
            rel="noopener noreferrer"
            className="text-cream underline underline-offset-2 hover:text-clay transition"
          >
            靈境智造 Intelliverse
          </a>
          <span className="mx-2 text-sand/40">·</span>
          <span className="text-sand/90">讓 AI 幫你賺錢</span>
        </div>
      </div>
    </footer>
  );
}
