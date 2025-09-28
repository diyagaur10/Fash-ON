import React from "react";
import logo from "../assets/logo.png"; // Place your logo image in src/assets/logo.png

function Navbar() {
  return (
    <nav className="w-full flex items-center justify-between py-3 px-6 bg-orange-300 shadow-md font-sans fixed top-0 left-0 z-50">
      <div className="flex items-center gap-0.1">
        <img src={logo} alt="FashON Logo" className="h-11 w-11 object-contain " />
        <span className="text-2xl font-bold text-white tracking-tight ml-1 font-caprasimo">FashON</span>
      </div>
      <div className="flex gap-6 text-white text-base font-medium">
        <a href="#" className="hover:text-peach transition font-caprasimo">Home</a>
        <a href="#" className="hover:text-peach transition font-caprasimo">New Arrivals</a>
        <a href="#about" className="hover:text-peach transition font-caprasimo">About</a>
        <a href="#contact" className="hover:text-peach transition font-caprasimo">Contact</a>
      </div>
    </nav>
  );
}

export default Navbar;
