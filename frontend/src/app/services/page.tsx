import Link from "next/link";

const services = [
  {
    id: 1,
    title: "کوتاهی مو",
    desc: "استایل حرفه‌ای و مدرن",
  },
  {
    id: 2,
    title: "رنگ مو",
    desc: "تکنیک‌های تخصصی رنگ",
  },
  {
    id: 3,
    title: "میکاپ",
    desc: "آرایش حرفه‌ای مراسم",
  },
];

export default function ServicesPage() {
  return (
    <main className="min-h-screen bg-[#0B0B0B] px-6 py-32 text-white">
      <div className="mx-auto max-w-6xl">
        <div className="mb-16 text-center">
          <p className="mb-4 text-sm tracking-[0.3em] text-[#D4B483]">
            خدمات ما
          </p>

          <h1 className="text-5xl font-semibold">
            خدمات تخصصی سالن
          </h1>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {services.map((service) => (
            <Link
              key={service.id}
              href={`/services/${service.id}`}
              className="group rounded-3xl border border-white/10 bg-white/5 p-8 transition hover:border-white/20"
            >
              <h2 className="text-2xl font-medium transition group-hover:text-[#D4B483]">
                {service.title}
              </h2>

              <p className="mt-4 leading-7 text-zinc-400">
                {service.desc}
              </p>

              <div className="mt-8 text-sm text-[#D4B483]">
                مشاهده جزئیات →
              </div>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}