import LandingCard from '../components/LandingCard';

export default function LandingPage() {
  return (
    <div
      className="h-screen w-full bg-cover bg-center flex items-center justify-center"
      style={{ backgroundImage: "url('/assets/earth.jpg')" }}
    >
      <div className="bg-black bg-opacity-60 p-6 rounded-xl">
        <LandingCard />
      </div>
    </div>
  );
}
