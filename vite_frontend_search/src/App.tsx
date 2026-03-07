import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Results from './pages/Results';
import AiSearchMode from './pages/AiSearchMode';

// Yeni Sayfalar
import About from './pages/About';
import Contact from './pages/Contact';
import HowItWorks from './pages/HowItWorks';
import Privacy from './pages/Privacy';
import Terms from './pages/Terms';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Ana Sayfa */}
        <Route path="/" element={<Home />} />
        
        {/* Sonuç Sayfası: /search?q=sorgu */}
        <Route path="/search" element={<Results />} />

        {/* YENİ: AI Mode Chat Sayfası */}
        <Route path="/ai" element={<AiSearchMode />} />


        {/* Statik Bilgi Sayfaları */}
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
        <Route path="/privacy" element={<Privacy />} />
        <Route path="/terms" element={<Terms />} />
      </Routes>
    </BrowserRouter>
  );
}