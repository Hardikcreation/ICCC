import React from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
    const navigate = useNavigate();

    return (
        <div style={{ textAlign: "center", marginTop: "100px" }}>
            <h1>Welcome to Smart Analysis Dashboard</h1>
            <button
                onClick={() => navigate("/facebook-analysis")}
                style={{ padding: "12px 24px", fontSize: "18px", marginTop: "20px" }}
            >
                Facebook Analysis
            </button>
        </div>
    );
};

export default Home;
