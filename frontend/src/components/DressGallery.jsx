import React from "react";

const images = [
  // Use relative paths from the public folder for local images
  "/assets/gallary_images/0e54af90dcf0f9a2b05f5f32f3dc869f.webp",
  "/assets/gallary_images/1adef7abe45fb32c8ece1a3abfefb1ca.webp",
  "/assets/gallary_images/06d108ca9a9eac71.jpg",
  "/assets/gallary_images/068eb67f78c4973f5e968c7aec2863ef.webp",
  "/assets/gallary_images/74b481f36fff6d17a0e5f19c7a3e7c47.webp",
  "/assets/gallary_images/0620ec1971b2f92c9d831f2d4c00c4a0.webp"
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
