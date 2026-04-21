import productsData from './products.json';

export type Course = {
  slug: string;
  category: string;
  title: string;
  duration: string;
  priceFrom: number;
  desc: string;
  cover: string;
};

export const courses: Course[] = [
  { slug: 'container-candle', category: 'A · 蠟燭系列', title: '容器蠟燭手作工作坊', duration: '2–2.5 小時', priceFrom: 980, desc: '從挑選香氣、調色到灌製，一次完成屬於自己的療癒燭光。', cover: 'from-sand to-clay/40' },
  { slug: 'soywax-advanced', category: 'A · 蠟燭系列', title: '大豆蠟香氛蠟燭進階班', duration: '3 小時', priceFrom: 1480, desc: '進階配方、分層設計、香調組合；適合已有基礎的學員。', cover: 'from-sand to-moss/30' },
  { slug: 'personal-perfume', category: 'B · 精油調香', title: '個人香水調製工作坊', duration: '2–2.5 小時', priceFrom: 1280, desc: '由芳療師引導，從前中後調打造 30ml 專屬香水。', cover: 'from-cream to-clay/50' },
  { slug: 'home-diffuser', category: 'B · 精油調香', title: '居家空間擴香調製', duration: '2 小時', priceFrom: 1180, desc: '依空間氛圍挑選精油，調出一款適合你家的味道。', cover: 'from-sand to-forest/20' },
  { slug: 'natural-skin-oil', category: 'B · 精油調香', title: '天然護膚油調製', duration: '2 小時', priceFrom: 1380, desc: '從基底油到精油比例，打造溫和親膚的日常保養油。', cover: 'from-cream to-moss/25' },
  { slug: 'crystal-perfume', category: 'B · 精油調香', title: '開運香氣 × 水晶香水', duration: '2 小時', priceFrom: 1580, desc: '結合水晶能量與香氣意象，為新階段儀式感加分。', cover: 'from-sand to-clay/30' },
  { slug: 'bath-bomb', category: 'C · 生活手作', title: '香氛沐浴球手作', duration: '1.5 小時', priceFrom: 780, desc: '繽紛泡湯時光，一次帶走 6 顆手作沐浴球。', cover: 'from-cream to-clay/40' },
  { slug: 'cold-soap', category: 'C · 生活手作', title: '手工皂冷製工作坊', duration: '2.5–3 小時', priceFrom: 1380, desc: '從油脂配方到脫模技巧，學會一塊溫和好用的冷製皂。', cover: 'from-sand to-moss/25' },
  { slug: 'solid-perfume', category: 'C · 生活手作', title: '固體香水 / 香膏製作', duration: '1.5 小時', priceFrom: 880, desc: '隨身攜帶的小型香氣儀式，適合送禮自用兩相宜。', cover: 'from-cream to-forest/20' },
];

// ---------- Products (from Excel + image folder) ----------

export type Product = {
  code: string;
  series: string | null;
  fullName: string;
  shortName: string;
  price: string | number | null;
  benefits: string | null;
  audience: string | null;
  ingredients: string | null;
  usage: string | null;
  usp: string | null;
  notes: string | null;
  category: string; // image category: 精油類 / 其他 / 臉部保養
  folder: string;
  image: string | null;
};

export const products: Product[] = productsData as Product[];

// Clean display name: drop "【澳維花園Aus Garden】" prefix and leading size; keep core name
export function displayName(p: Product): string {
  const n = (p.fullName || p.shortName || p.code).toString();
  return n.replace(/【[^】]*】\s*/g, '').trim();
}

// Normalise price to number or null
export function priceNumber(p: Product): number | null {
  if (p.price == null) return null;
  if (typeof p.price === 'number') return p.price;
  const m = String(p.price).replace(/[^0-9.]/g, '');
  return m ? Number(m) : null;
}

export const productCategories = ['全部', '精油類', '臉部保養', '其他'] as const;
