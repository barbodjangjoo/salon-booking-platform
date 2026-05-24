export default function HomePage() {
  return (
    <main className="min-h-screen bg-[#0B0B0B] text-white">
      <section className="flex min-h-screen items-center justify-center px-6">
        <div className="text-center">
          <p className="mb-4 text-sm tracking-[0.3em] text-[#D4B483]">
            تجربه لوکس زیبایی
          </p>

          <h1 className="max-w-5xl text-5xl leading-tight font-semibold tracking-tight md:text-8xl">
            زیبایی مدرن،
            <br />
            تجربه‌ای متفاوت
          </h1>

          <p className="mx-auto mt-8 max-w-2xl text-lg leading-8 text-zinc-400">
            رزرو آنلاین خدمات سالن با تجربه‌ای مینیمال، سریع و مدرن برای
            مشتریانی که به کیفیت اهمیت می‌دهند.
          </p>

          <div className="mt-12 flex items-center justify-center gap-4">
            <button className="rounded-full bg-[#D4B483] px-8 py-4 text-sm font-medium text-black transition hover:scale-[1.02]">
              رزرو نوبت
            </button>

            <button className="rounded-full border border-zinc-800 px-8 py-4 text-sm font-medium transition hover:border-zinc-600">
              مشاهده خدمات
            </button>
          </div>
        </div>
      </section>
    </main>
  );
}