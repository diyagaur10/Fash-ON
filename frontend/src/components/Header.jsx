import React from "react";

function Header() {
  return (
    <header className="w-full flex flex-col items-center py-8">
      <h1 className="text-5xl font-bold text-gray-900 mb-2 tracking-tight">
        <span className="bg-peachDark px-4 py-2 rounded-xl font-caprasimo">FashON</span>
        <br/>
        <span className="ml-2 text-peachDark font-caprasimo">AI Fashion Search</span>
      </h1>
      <p className="text-lg text-gray-500 font-caprasimo">Find your next look with AI-powered image search</p>
    </header>
  );
}

export default Header;
