import React from "react";

const socialLinks = [
  {
    href: "https://instagram.com/",
    label: "Instagram",
    icon: (
      <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
        <rect width="20" height="20" x="2" y="2" rx="6" fill="none" stroke="currentColor" strokeWidth="1.5"/>
        <circle cx="12" cy="12" r="5" stroke="currentColor" strokeWidth="1.5" fill="none"/>
        <circle cx="17" cy="7" r="1.2" fill="currentColor"/>
      </svg>
    ),
  },
  {
    href: "https://linkedin.com/",
    label: "LinkedIn",
    icon: (
      <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
        <rect width="20" height="20" x="2" y="2" rx="4" fill="none" stroke="currentColor" strokeWidth="1.5"/>
        <rect x="7" y="10" width="2" height="7" fill="currentColor"/>
        <rect x="11" y="13" width="2" height="4" fill="currentColor"/>
        <circle cx="8" cy="8" r="1" fill="currentColor"/>
      </svg>
    ),
  },
  {
    href: "https://pinterest.com/",
    label: "Pinterest",
    icon: (
      <svg fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
        <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="1.5" fill="none"/>
        <path d="M12 17c2.5 0 4.5-2 4.5-4.5S14.5 8 12 8s-4.5 2-4.5 4.5c0 1.5.8 2.8 2 3.5" stroke="currentColor" strokeWidth="1.5"/>
        <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
      </svg>
    ),
  },
];

const bottomLinks = [
  { label: "Privacy", href: "#" },
  { label: "Terms", href: "#" },
  { label: "Support", href: "#" },
  { label: "Contact Us", href: "#contact" },
];

function Footer() {
  return (
    <footer className="bg-[#FFF9F7] w-full py-8 px-4 border-t border-peach flex flex-col items-center z-40 mt-16">
      <div className="text-center text-peachDark text-lg font-semibold mb-3">
        Built with love and style ✨ FashON
      </div>
      {/*<div className="flex gap-6 mb-4">
        {socialLinks.map((link) => (
          <a
            key={link.label}
            href={link.href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-peachDark hover:text-peach transition-colors"
            aria-label={link.label}
          >
            {link.icon}
          </a>
        ))}
      </div> */ }
      <div className="flex flex-wrap gap-4 justify-center text-gray-400 text-sm border-t border-peach pt-3 w-full max-w-xl">
        {bottomLinks.map((link, i) => (
          <React.Fragment key={link.label}>
            <a href={link.href} className="hover:text-peachDark transition-colors">{link.label}</a>
            {i < bottomLinks.length - 1 && <span className="mx-1">|</span>}
          </React.Fragment>
        ))}
      </div>
    </footer>
  );
}

export default Footer;
