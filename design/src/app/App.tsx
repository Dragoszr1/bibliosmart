import { useState } from "react";
import { Search, Clock, BookOpen, Cpu, Database, Terminal, Globe, ChevronRight, ArrowRight, Monitor, Wifi, BookMarked, Bell, Menu, X, ExternalLink, Calendar } from "lucide-react";

const NAV_LINKS = ["Catalog", "Digital Resources", "Events", "About", "Contact"];

const FEATURED_BOOKS = [
  {
    id: 1,
    title: "Clean Code",
    author: "Robert C. Martin",
    year: 2008,
    genre: "Software Engineering",
    cover: "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=200&h=280&fit=crop&auto=format",
    available: true,
    copies: 3,
  },
  {
    id: 2,
    title: "The Pragmatic Programmer",
    author: "Andrew Hunt & David Thomas",
    year: 2019,
    genre: "Career & Craft",
    cover: "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=200&h=280&fit=crop&auto=format",
    available: true,
    copies: 2,
  },
  {
    id: 3,
    title: "Computer Networks",
    author: "Andrew S. Tanenbaum",
    year: 2021,
    genre: "Networking",
    cover: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=200&h=280&fit=crop&auto=format",
    available: false,
    copies: 0,
  },
  {
    id: 4,
    title: "Introduction to Algorithms",
    author: "Cormen, Leiserson, Rivest",
    year: 2022,
    genre: "Algorithms",
    cover: "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=200&h=280&fit=crop&auto=format",
    available: true,
    copies: 1,
  },
  {
    id: 5,
    title: "Operating System Concepts",
    author: "Abraham Silberschatz",
    year: 2020,
    genre: "Systems",
    cover: "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=200&h=280&fit=crop&auto=format",
    available: true,
    copies: 4,
  },
];

const DIGITAL_RESOURCES = [
  { icon: <Globe size={22} />, name: "IEEE Xplore", desc: "Engineering & CS journals", tag: "Academic" },
  { icon: <Monitor size={22} />, name: "O'Reilly Learning", desc: "Technical books & videos", tag: "Books" },
  { icon: <Database size={22} />, name: "Springer Link", desc: "Computer science research papers", tag: "Research" },
  { icon: <Terminal size={22} />, name: "Codecademy Pro", desc: "Interactive coding courses", tag: "Learning" },
  { icon: <Wifi size={22} />, name: "Cisco NetAcad", desc: "Networking certifications", tag: "Certs" },
  { icon: <Cpu size={22} />, name: "ACM Digital Library", desc: "Computing literature archive", tag: "Academic" },
];


const HOURS = [
  { day: "Monday – Friday", hours: "08:00 – 20:00" },
  { day: "Saturday", hours: "09:00 – 16:00" },
  { day: "Sunday", hours: "Closed" },
];

const GOLD = "#c9a84c";
const GOLD_LIGHT = "rgba(201,168,76,0.18)";
const GOLD_BORDER = "rgba(201,168,76,0.35)";
const CREAM = "#f9f0e1";
const CREAM_DARK = "#ede0cc";
const MAROON = "#9B1B30";
const DEEP = "#2D1018";
const INK = "#2a1410";
const INK_MUTED = "#7a5a55";

function Badge({ text, variant = "default" }: { text: string; variant?: "default" | "green" | "red" | "gold" | "blue" }) {
  const classes: Record<string, string> = {
    default: "bg-secondary text-muted-foreground",
    green: "bg-[#2a5c3a]/60 text-[#6fcf97] border border-[#6fcf97]/30",
    red: "bg-[#ff3d5a]/10 text-[#ff3d5a] border border-[#ff3d5a]/30",
    gold: `border text-[#c9a84c]`,
    blue: "bg-[#9B1B30]/40 text-[#f5a0ac] border border-[#9B1B30]/60",
  };
  return (
    <span
      className={`font-mono text-[10px] tracking-widest uppercase px-2 py-0.5 rounded-sm ${classes[variant]}`}
      style={variant === "gold" ? { backgroundColor: GOLD_LIGHT, borderColor: GOLD_BORDER } : undefined}
    >
      {text}
    </span>
  );
}

export default function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [activeFilter, setActiveFilter] = useState("All");

  const filters = ["All", "Software", "Networking", "Algorithms", "Systems", "Career"];

  return (
    <div className="min-h-screen bg-background text-foreground" style={{ fontFamily: "'Inter', sans-serif" }}>
      {/* Nav */}
      <nav className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-sm flex items-center justify-center" style={{ backgroundColor: GOLD }}>
              <BookMarked size={16} className="text-[#2D1018]" />
            </div>
            <div>
              <span
                className="text-foreground font-black text-lg leading-none tracking-tight"
                style={{ fontFamily: "'Barlow Condensed', sans-serif" }}
              >
                IT HIGH SCHOOL
              </span>
              <p className="font-mono text-[10px] tracking-widest uppercase leading-none mt-0.5" style={{ color: GOLD }}>
                Library System
              </p>
            </div>
          </div>

          <div className="hidden md:flex items-center gap-8">
            {NAV_LINKS.map((link) => (
              <a
                key={link}
                href="#"
                className="font-mono text-xs tracking-wider text-muted-foreground hover:text-foreground transition-colors uppercase"
              >
                {link}
              </a>
            ))}
          </div>

          <div className="hidden md:flex items-center gap-3">
            <button
              className="flex items-center gap-2 px-4 py-2 rounded-sm text-xs font-mono tracking-wider uppercase transition-colors text-[#2D1018]"
              style={{ backgroundColor: GOLD }}
            >
              <BookOpen size={13} />
              My Account
            </button>
          </div>

          <button className="md:hidden text-foreground" onClick={() => setMenuOpen(!menuOpen)}>
            {menuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>

        {menuOpen && (
          <div className="md:hidden border-t border-border bg-card px-6 py-4 flex flex-col gap-4">
            {NAV_LINKS.map((link) => (
              <a
                key={link}
                href="#"
                className="font-mono text-xs tracking-wider text-muted-foreground uppercase"
              >
                {link}
              </a>
            ))}
            <button
              className="flex items-center gap-2 px-4 py-2 rounded-sm text-xs font-mono tracking-wider uppercase w-fit text-[#2D1018]"
              style={{ backgroundColor: GOLD }}
            >
              <BookOpen size={13} />
              My Account
            </button>
          </div>
        )}
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden border-b border-border min-h-[560px] flex items-center">
        {/* Bookshelf background */}
        <img
          src="https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=1600&h=900&fit=crop&auto=format"
          alt="Library bookshelves"
          className="absolute inset-0 w-full h-full object-cover object-center"
        />
        {/* Dark maroon gradient overlay — left heavy so text is legible, right fades to show shelves */}
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(105deg, rgba(45,16,24,0.97) 0%, rgba(45,16,24,0.88) 45%, rgba(45,16,24,0.55) 70%, rgba(45,16,24,0.3) 100%)",
          }}
        />
        {/* Subtle grid on top */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage:
              "repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(201,168,76,1) 39px, rgba(201,168,76,1) 40px), repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(201,168,76,1) 39px, rgba(201,168,76,1) 40px)",
          }}
        />

        <div className="max-w-7xl mx-auto px-6 py-24 md:py-32 relative w-full">
          <div className="max-w-2xl">
            <div className="flex items-center gap-2 mb-6">
              <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: GOLD }} />
              <span className="font-mono text-xs tracking-widest uppercase" style={{ color: GOLD }}>
                Library — Open Now
              </span>
            </div>
            <h1
              className="text-7xl md:text-9xl font-black leading-none tracking-tight text-white mb-6"
              style={{ fontFamily: "'Barlow Condensed', sans-serif" }}
            >
              EXPLORE.
              <br />
              <span style={{ color: GOLD }}>LEARN.</span>
              <br />
              BUILD.
            </h1>
            <p className="text-white/70 text-base leading-relaxed max-w-md mb-10">
              Your gateway to 12,000+ technical books, digital journals, and learning resources. Built for the
              students and teachers of the IT High School community.
            </p>
            <div className="flex flex-col sm:flex-row gap-3">
              <button
                className="flex items-center justify-center gap-2 px-6 py-3 text-sm font-mono tracking-wider uppercase transition-opacity hover:opacity-90 rounded-sm text-[#2D1018]"
                style={{ backgroundColor: GOLD }}
              >
                Browse Catalog <ArrowRight size={15} />
              </button>
              <button className="flex items-center justify-center gap-2 border border-white/25 text-white px-6 py-3 text-sm font-mono tracking-wider uppercase hover:border-white/50 transition-colors rounded-sm backdrop-blur-sm">
                Digital Resources
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Search & Catalog */}
      <section style={{ backgroundColor: CREAM, borderBottom: `1px solid ${CREAM_DARK}` }}>
        <div className="max-w-7xl mx-auto px-6 py-16">
          <div className="flex flex-col md:flex-row md:items-end gap-6 mb-10">
            <div className="flex-1">
              <p className="font-mono text-xs tracking-widest uppercase mb-2" style={{ color: MAROON }}>
                // Book Catalog
              </p>
              <h2
                className="text-4xl font-black tracking-tight"
                style={{ fontFamily: "'Barlow Condensed', sans-serif", color: INK }}
              >
                NEW & FEATURED TITLES
              </h2>
            </div>
            <div className="relative w-full md:w-80">
              <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2" style={{ color: INK_MUTED }} />
              <input
                type="text"
                placeholder="Search by title, author, ISBN..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-4 py-2.5 text-sm font-mono rounded-sm focus:outline-none"
                style={{
                  backgroundColor: CREAM_DARK,
                  border: `1px solid rgba(42,20,16,0.15)`,
                  color: INK,
                }}
              />
            </div>
          </div>

          {/* Filters */}
          <div className="flex gap-2 flex-wrap mb-8">
            {filters.map((f) => (
              <button
                key={f}
                onClick={() => setActiveFilter(f)}
                className="font-mono text-xs px-4 py-1.5 rounded-sm uppercase tracking-wider border transition-colors"
                style={
                  activeFilter === f
                    ? { backgroundColor: MAROON, color: "#fff", borderColor: MAROON }
                    : { backgroundColor: "transparent", borderColor: "rgba(42,20,16,0.2)", color: INK_MUTED }
                }
              >
                {f}
              </button>
            ))}
          </div>

          {/* Book Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-5">
            {FEATURED_BOOKS.map((book) => (
              <div
                key={book.id}
                className="group rounded-sm overflow-hidden cursor-pointer transition-all"
                style={{
                  border: `1px solid rgba(42,20,16,0.12)`,
                  backgroundColor: "#fff",
                  boxShadow: "0 1px 4px rgba(42,20,16,0.06)",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.boxShadow = "0 4px 16px rgba(155,27,48,0.12)")}
                onMouseLeave={(e) => (e.currentTarget.style.boxShadow = "0 1px 4px rgba(42,20,16,0.06)")}
              >
                <div className="relative overflow-hidden h-44" style={{ backgroundColor: CREAM_DARK }}>
                  <img
                    src={book.cover}
                    alt={`Cover of ${book.title}`}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute top-2 right-2">
                    {book.available ? (
                      <Badge text="Available" variant="green" />
                    ) : (
                      <Badge text="Out" variant="red" />
                    )}
                  </div>
                </div>
                <div className="p-3">
                  <p className="font-mono text-[10px] uppercase tracking-wider mb-1" style={{ color: INK_MUTED }}>
                    {book.genre}
                  </p>
                  <h3 className="text-sm font-semibold leading-tight mb-1 line-clamp-2" style={{ color: INK }}>
                    {book.title}
                  </h3>
                  <p className="text-xs" style={{ color: INK_MUTED }}>{book.author}</p>
                  {book.available && (
                    <p className="font-mono text-[10px] mt-2" style={{ color: MAROON }}>
                      {book.copies} copies left
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-8 text-center">
            <button
              className="font-mono text-xs uppercase tracking-widest hover:underline flex items-center gap-1 mx-auto"
              style={{ color: MAROON }}
            >
              View Full Catalog <ChevronRight size={13} />
            </button>
          </div>
        </div>
      </section>

      {/* Digital Resources */}
      <section style={{ backgroundColor: CREAM_DARK, borderBottom: `1px solid rgba(42,20,16,0.12)` }}>
        <div className="max-w-7xl mx-auto px-6 py-16">
          <div className="mb-10">
            <p className="font-mono text-xs tracking-widest uppercase mb-2" style={{ color: MAROON }}>
              // Remote Access
            </p>
            <h2
              className="text-4xl font-black tracking-tight"
              style={{ fontFamily: "'Barlow Condensed', sans-serif", color: INK }}
            >
              DIGITAL RESOURCES
            </h2>
            <p className="text-sm mt-2 max-w-lg" style={{ color: INK_MUTED }}>
              Access all platforms with your school credentials from anywhere, 24/7.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {DIGITAL_RESOURCES.map((res) => (
              <div
                key={res.name}
                className="group rounded-sm p-5 flex items-start gap-4 cursor-pointer transition-all"
                style={{
                  backgroundColor: "#fff",
                  border: `1px solid rgba(42,20,16,0.1)`,
                  boxShadow: "0 1px 3px rgba(42,20,16,0.05)",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.boxShadow = "0 4px 14px rgba(155,27,48,0.1)")}
                onMouseLeave={(e) => (e.currentTarget.style.boxShadow = "0 1px 3px rgba(42,20,16,0.05)")}
              >
                <div
                  className="shrink-0 w-10 h-10 rounded-sm flex items-center justify-center"
                  style={{ backgroundColor: GOLD_LIGHT, border: `1px solid ${GOLD_BORDER}`, color: GOLD }}
                >
                  {res.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="text-sm font-semibold" style={{ color: INK }}>{res.name}</h3>
                    <Badge text={res.tag} variant="gold" />
                  </div>
                  <p className="text-xs" style={{ color: INK_MUTED }}>{res.desc}</p>
                </div>
                <ExternalLink size={14} className="shrink-0 mt-0.5 transition-colors" style={{ color: "rgba(42,20,16,0.25)" }} />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Hours & Info */}
      <section style={{ backgroundColor: CREAM, borderBottom: `1px solid ${CREAM_DARK}` }}>
        <div className="max-w-7xl mx-auto px-6 py-16">
          <div className="mb-10">
            <p className="font-mono text-xs tracking-widest uppercase mb-2" style={{ color: MAROON }}>
              // Library Info
            </p>
            <h2
              className="text-4xl font-black tracking-tight"
              style={{ fontFamily: "'Barlow Condensed', sans-serif", color: INK }}
            >
              VISIT US
            </h2>
          </div>

          <div className="grid lg:grid-cols-3 gap-6">
            {/* Hours */}
            <div
              className="rounded-sm p-6"
              style={{ backgroundColor: "#fff", border: `1px solid rgba(42,20,16,0.1)` }}
            >
              <div className="flex items-center gap-2 mb-5">
                <Clock size={15} style={{ color: MAROON }} />
                <p className="font-mono text-xs tracking-widest uppercase" style={{ color: MAROON }}>
                  Opening Hours
                </p>
              </div>
              <div className="flex flex-col gap-3">
                {HOURS.map((h) => (
                  <div
                    key={h.day}
                    className="flex justify-between items-center pb-3 last:pb-0"
                    style={{ borderBottom: `1px solid rgba(42,20,16,0.08)` }}
                  >
                    <span className="font-mono text-xs uppercase tracking-wide" style={{ color: INK_MUTED }}>
                      {h.day}
                    </span>
                    <span
                      className="font-mono text-xs font-medium"
                      style={{ color: h.hours === "Closed" ? "#c0392b" : INK }}
                    >
                      {h.hours}
                    </span>
                  </div>
                ))}
              </div>
              <div
                className="mt-5 flex items-center gap-2 rounded-sm px-3 py-2"
                style={{ backgroundColor: GOLD_LIGHT, border: `1px solid ${GOLD_BORDER}` }}
              >
                <div className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ backgroundColor: GOLD }} />
                <span className="font-mono text-xs tracking-wider" style={{ color: "#8a6a20" }}>
                  Currently Open
                </span>
              </div>
            </div>

            {/* Notices */}
            <div
              className="rounded-sm p-6"
              style={{ backgroundColor: "#fff", border: `1px solid rgba(42,20,16,0.1)` }}
            >
              <div className="flex items-center gap-2 mb-4">
                <Bell size={14} style={{ color: MAROON }} />
                <p className="font-mono text-xs tracking-widest uppercase" style={{ color: MAROON }}>
                  Notices
                </p>
              </div>
              <ul className="flex flex-col gap-4">
                <li
                  className="text-xs leading-relaxed pl-3"
                  style={{ borderLeft: `2px solid ${MAROON}`, color: INK_MUTED }}
                >
                  Loan period extended to 21 days for exam period (Aug 1 – Sep 15).
                </li>
                <li
                  className="text-xs leading-relaxed pl-3"
                  style={{ borderLeft: `2px solid rgba(42,20,16,0.15)`, color: INK_MUTED }}
                >
                  New batch of hardware reference books added to Section C.
                </li>
                <li
                  className="text-xs leading-relaxed pl-3"
                  style={{ borderLeft: `2px solid rgba(42,20,16,0.15)`, color: INK_MUTED }}
                >
                  IEEE Xplore access renewed — full-text available for all students.
                </li>
              </ul>
            </div>

            {/* Quick links */}
            <div
              className="rounded-sm p-6"
              style={{ backgroundColor: "#fff", border: `1px solid rgba(42,20,16,0.1)` }}
            >
              <p className="font-mono text-xs tracking-widest uppercase mb-4" style={{ color: INK_MUTED }}>
                Quick Links
              </p>
              {[
                { label: "Reserve a Study Room", icon: <Calendar size={13} /> },
                { label: "Request a Book", icon: <BookOpen size={13} /> },
                { label: "Report a Lost Book", icon: <Bell size={13} /> },
                { label: "Contact Librarian", icon: <ChevronRight size={13} /> },
              ].map((link) => (
                <a
                  key={link.label}
                  href="#"
                  className="flex items-center justify-between py-2.5 text-xs transition-colors group"
                  style={{ borderBottom: `1px solid rgba(42,20,16,0.08)`, color: INK }}
                  onMouseEnter={(e) => (e.currentTarget.style.color = MAROON)}
                  onMouseLeave={(e) => (e.currentTarget.style.color = INK)}
                >
                  <span className="flex items-center gap-2">
                    {link.icon}
                    {link.label}
                  </span>
                  <ChevronRight size={13} style={{ color: "rgba(42,20,16,0.3)" }} />
                </a>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ backgroundColor: DEEP, borderTop: `1px solid rgba(255,255,255,0.08)` }}>
        <div className="max-w-7xl mx-auto px-6 py-10">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-10">
            <div className="col-span-2 md:col-span-1">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded-sm flex items-center justify-center" style={{ backgroundColor: GOLD }}>
                  <BookMarked size={12} style={{ color: DEEP }} />
                </div>
                <span
                  className="font-black text-base text-white"
                  style={{ fontFamily: "'Barlow Condensed', sans-serif" }}
                >
                  ITSHS LIBRARY
                </span>
              </div>
              <p className="text-xs leading-relaxed" style={{ color: "rgba(255,255,255,0.45)" }}>
                Serving the IT High School community since 2003. Building the next generation of technologists, one
                book at a time.
              </p>
            </div>

            {[
              {
                title: "Services",
                links: ["Book Borrowing", "Digital Access", "Study Rooms", "Research Help", "Interlibrary Loan"],
              },
              {
                title: "Resources",
                links: ["Book Catalog", "E-Journals", "Databases", "Thesis Archive", "Reading Lists"],
              },
              {
                title: "Info",
                links: ["About the Library", "Staff Directory", "Library Policies", "Accessibility", "Feedback"],
              },
            ].map((col) => (
              <div key={col.title}>
                <p className="font-mono text-[11px] uppercase tracking-widest mb-3" style={{ color: GOLD }}>
                  {col.title}
                </p>
                <ul className="flex flex-col gap-2">
                  {col.links.map((l) => (
                    <li key={l}>
                      <a
                        href="#"
                        className="text-xs transition-colors"
                        style={{ color: "rgba(255,255,255,0.45)" }}
                        onMouseEnter={(e) => (e.currentTarget.style.color = "rgba(255,255,255,0.85)")}
                        onMouseLeave={(e) => (e.currentTarget.style.color = "rgba(255,255,255,0.45)")}
                      >
                        {l}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <div
            className="pt-6 flex flex-col sm:flex-row justify-between gap-3 items-center"
            style={{ borderTop: `1px solid rgba(255,255,255,0.08)` }}
          >
            <p className="font-mono text-[11px]" style={{ color: "rgba(255,255,255,0.35)" }}>
              © 2026 IT High School Library. All rights reserved.
            </p>
            <p className="font-mono text-[11px]" style={{ color: "rgba(255,255,255,0.35)" }}>
              <span style={{ color: GOLD }}>SYS_STATUS:</span> Online · v3.2.1
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
