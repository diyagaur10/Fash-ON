import React from "react";
import { Upload } from "lucide-react";

function ImageUpload({ file, setFile, onSearch, loading }) {
  return (
    <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-lg text-center border border-peachDark">
      <input
        type="file"
        accept="image/*"
        onChange={e => setFile(e.target.files[0])}
        className="mb-4 block w-full text-sm text-gray-600
                   file:mr-4 file:py-2 file:px-4
                   file:rounded-full file:border-0
                   file:text-sm file:font-semibold
                   file:bg-peach file:text-peachDark
                   hover:file:bg-peachDark cursor-pointer"
      />
      <button
        onClick={onSearch}
        disabled={loading}
        className="bg-peachDark text-white px-8 py-3 rounded-xl flex items-center justify-center mx-auto hover:bg-peach transition disabled:opacity-50"
      >
        {loading ? (
          "Searching..."
        ) : (
          <>
            <Upload className="mr-2" size={18} /> Search 
          </>
        )}
      </button>
    </div>
  );
}

export default ImageUpload;
