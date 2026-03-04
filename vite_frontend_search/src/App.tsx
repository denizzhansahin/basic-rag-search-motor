import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Results from './components/Results';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Ana Sayfa */}
        <Route path="/" element={<Home />} />
        
        {/* Sonuç Sayfası: /search?q=sorgu */}
        <Route path="/search" element={<Results />} />
      </Routes>
    </BrowserRouter>
  );
}