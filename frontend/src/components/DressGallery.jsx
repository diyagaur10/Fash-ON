import React from "react";

const images = [
  // Replace these URLs with your own dress images or use Unsplash/placeholder links
  "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=400&q=80",
  "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=400&q=80",
  "https://images.unsplash.com/photo-1469398715555-76331a6c7c9b?auto=format&fit=crop&w=400&q=80",
  "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=400&q=80",
  "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=400&q=80",
  "https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=crop&w=400&q=80"
];

function DressGallery() {
  return (
    <div className="w-screen flex flex-col items-center my-10 overflow-x-hidden">
      <h2 className="text-2xl font-bold text-peachDark mb-6 font-caprasimo">Trending Dresses</h2>
      <div className="relative w-screen h-80 overflow-x-hidden">
        <div className="absolute left-0 top-0 flex h-80 animate-marquee gap-6">
          {images.concat(images).map((src, i) => (
            <div
              key={i}
              className="relative group overflow-hidden rounded-2xl shadow-lg hover:scale-105 hover:shadow-2xl transition-all duration-300 bg-white"
              style={{ aspectRatio: '3/4', minWidth: '200px', maxWidth: '220px' }}
            >
              <img
                src={src}
                alt={`Dress ${i+1}`}
                className="w-full h-full object-cover group-hover:blur-[2px] group-hover:brightness-90 transition-all duration-300"
              />
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 bg-black/30">
                <span className="text-white text-lg font-semibold">View Details</span>
              </div>
            </div>
          ))}
        </div>
      </div>
      <style>{`
        @keyframes marquee {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-marquee {
          animation: marquee 30s linear infinite;
        }
      `}</style>
    </div>
  );
}

export default DressGallery;
