import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Facebook from "./pages/Facebook";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/facebook-analysis" element={<Facebook />} /> {/* ✅ This line */}
      </Routes>
    </Router>
  );
}

export default App;
