import React, { useEffect, useRef } from "react";
function DynamicBg() {
  const waveRef = useRef(null);
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (waveRef.current) {
        const x = e.clientX;
        const y = e.clientY;
        waveRef.current.style.left = `${x - 200}px`;
        waveRef.current.style.top = `${y - 200}px`;
      }
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);
  return (
    <div
      ref={waveRef}
      className="pointer-events-none fixed z-0 w-[400px] h-[400px] rounded-full bg-gradient-to-tr from-peachDark via-orange-300 to-peach opacity-60 blur-3xl transition-all duration-300"
      style={{
        left: "50vw",
        top: "50vh",
        transform: "translate(-50%, -50%)",
      }}
    />
  );
}
export default DynamicBg;