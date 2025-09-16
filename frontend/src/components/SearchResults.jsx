import React from "react";
import ProductCard from "./ProductCard";
import { motion } from "framer-motion";

function SearchResults({ results }) {
  return (
    <div className="w-full max-w-7xl mt-12 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
      {results.map((item, idx) => (
        <motion.div
          key={idx}
          className="h-full flex"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <ProductCard product={item.product} />
        </motion.div>
      ))}
    </div>
  );
}

export default SearchResults;
