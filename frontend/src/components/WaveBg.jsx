import React, { useEffect, useRef } from "react";

function WaveBg() {
  const waveRef = useRef(null);

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (waveRef.current) {
        // Move the wave horizontally with the cursor, but keep it subtle
        const x = e.clientX / window.innerWidth;
        waveRef.current.setAttribute(
          "d",
          `
            M0,320 
            C${200 + 100 * x},280 ${400 + 200 * x},360 ${800},320 
            L800,0 L0,0 Z
          `
        );
      }
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <svg
      className="fixed top-0 left-0 w-full h-[400px] z-0 pointer-events-none"
      viewBox="0 0 800 400"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ minWidth: "100vw" }}
    >
      <defs>
        <linearGradient id="waveGradient" x1="0" y1="0" x2="800" y2="400" gradientUnits="userSpaceOnUse">
          <stop stopColor="#FFDAB9" stopOpacity="0.8" />
          <stop offset="0.5" stopColor="#FFB88C" stopOpacity="0.7" />
          <stop offset="1" stopColor="#FFB347" stopOpacity="0.6" />
        </linearGradient>
      </defs>
      <path
        ref={waveRef}
        d="M0,320 C200,280 600,360 800,320 L800,0 L0,0 Z"
        fill="url(#waveGradient)"
        style={{ transition: "d 0.3s cubic-bezier(.4,0,.2,1)" }}
      />
    </svg>
  );
}

export default WaveBg;