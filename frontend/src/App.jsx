// src/App.jsx
//import DynamicBg from "./components/DynamicBg";
import React, { useState } from "react";
import axios from "axios";
import Header from "./components/Header";
import Navbar from "./components/Navbar";
import ImageUpload from "./components/ImageUpload";
import SearchResults from "./components/SearchResults";
import About from "./components/About";
import Contact from "./components/Contact";
import Footer from "./components/Footer";
import DressGallery from "./components/DressGallery";

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("top_k", 12);
    try {
      const res = await axios.post("http://127.0.0.1:8000/search/image", formData, { //fixed backend error
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResults(res.data);
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-peach flex flex-col items-center justify-center  p-6">
      <div className="flex flex-col items-center justify-center">
        {/* <DynamicBg /> */}
        <Navbar />
        <Header />
        
        <ImageUpload file={file} setFile={setFile} onSearch={handleSearch} loading={loading} />
        <SearchResults results={results} />
        <DressGallery />
        <About />
        <Contact />
        <Footer />
      </div>
    </div>
  );
}

export default App;
