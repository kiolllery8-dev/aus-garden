'use client';
import Link from 'next/link';
import { useState } from 'react';

const nav = [
  { href: '/', label: '首頁' },
  { href: '/courses', label: '手作課程' },
  { href: '/products', label: '香氛商品' },
  { href: '/about', label: '品牌故事' },
  { href: '/contact', label: '聯絡我們' },
];

export default function Header() {
  const [open, setOpen] = useState(false);
  return (
    <header className="sticky top-0 z-40 bg-cream/90 backdrop-blur border-b hairline">
      <div className="container flex items-center justify-between h-20">
        <Link href="/" className="flex flex-col leading-tight">
          <span className="font-serif text-xl tracking-widest text-forest">AUS GARDEN</span>
          <span className="text-[11px] tracking-[0.3em] text-moss">澳維花園</span>
        </Link>

        <nav className="hidden md:flex gap-10 text-sm">
          {nav.map((n) => (
            <Link key={n.href} href={n.href} className="hover:text-moss transition">
              {n.label}
            </Link>
          ))}
        </nav>

        <Link href="/contact" className="hidden md:inline-flex btn btn-primary">
          預約課程
        </Link>

        <button
          aria-label="menu"
          className="md:hidden p-2"
          onClick={() => setOpen(!open)}
        >
          <span className="block w-6 h-0.5 bg-forest mb-1.5" />
          <span className="block w-6 h-0.5 bg-forest mb-1.5" />
          <span className="block w-6 h-0.5 bg-forest" />
        </button>
      </div>

      {open && (
        <div className="md:hidden border-t hairline">
          <div className="container py-4 flex flex-col gap-3">
            {nav.map((n) => (
              <Link key={n.href} href={n.href} onClick={() => setOpen(false)}>
                {n.label}
              </Link>
            ))}
            <Link href="/contact" className="btn btn-primary mt-2" onClick={() => setOpen(false)}>
              預約課程
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
