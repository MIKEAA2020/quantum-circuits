import { SiteNav } from "@/components/sections/nav";
import { Hero } from "@/components/sections/hero";
import { ModelSection } from "@/components/sections/model-section";
import { SimulatorSection } from "@/components/sections/simulator-section";
import { FssSection } from "@/components/sections/fss-section";
import { ResultsSection } from "@/components/sections/results-section";
import { TheorySection } from "@/components/sections/theory-section";
import { ReplicaSection } from "@/components/sections/replica-section";
import { RecordScgfSection } from "@/components/sections/record-scgf-section";
import { ReproSection } from "@/components/sections/repro-section";
import { SiteFooter } from "@/components/sections/footer";
import { BackToTop } from "@/components/sections/back-to-top";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-zinc-950 text-zinc-100">
      <SiteNav />
      <main className="flex-1">
        <Hero />
        <ModelSection />
        <SimulatorSection />
        <FssSection />
        <ResultsSection />
        <TheorySection />
        <ReplicaSection />
        <RecordScgfSection />
        <ReproSection />
      </main>
      <SiteFooter />
      <BackToTop />
    </div>
  );
}
