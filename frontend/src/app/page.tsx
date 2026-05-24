import Navbar from "@/components/layout/navbar";
import HeroSection from "@/components/hero/hero-section";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-[#0B0B0B] text-white">
      <Navbar />

      <HeroSection />
    </main>
  );
}