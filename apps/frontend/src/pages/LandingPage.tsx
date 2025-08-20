import LandingCard from "../components/LandingCard";

export default function LandingPage() {
  return (
    <div
      className="h-screen w-full bg-cover bg-center flex items-center justify-center"
      style={{ backgroundImage: "url('/earth.jpg')" }}
    >
      <div className="bg-primary-blue bg-opacity-60 p-6 border-4 border-primary-red rounded-xl">
        <LandingCard />
      </div>
    </div>
  );
}
