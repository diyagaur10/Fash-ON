import React from "react";

function ProductCard({ product }) {
  return (
    <div className="bg-pink rounded-xl shadow-lg border border-peachDark overflow-hidden flex flex-col font-sans transition hover:scale-105 hover:shadow-2xl hover:bg-gray-200 hover:border-gray-200 h-full ">
      <img
        src={product.image_url}
        alt={product.title}
        className="w-full object-cover h-72"
        style={{ objectFit: "cover" }}
      />
      <div className="p-5 flex-1 flex flex-col items-center justify-between">
        <h2 className="text-lg font-bold mb-1 text-center text-gray-150">
          {product.title}
        </h2>
        <p className="text-purple font-semibold mb-1">{product.brand}</p>
        <p className="text-grayText font-bold mb-2">{product.price_raw}</p>
        <a
          href={product.product_url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-2 inline-block bg-peachDark text-white px-6 py-2 rounded-full hover:bg-peach transition font-bold shadow"
        >
          More Details
        </a>
      </div>
    </div>
  );
}

export default ProductCard;
