// src/services/api.js
import axios from "axios";

export const fetchFacebookPosts = async () => {
    try {
        const response = await axios.get("http://127.0.0.1:8000/api/facebook/posts");
        return response.data;
    } catch (err) {
        console.error("Error fetching posts:", err);
        return [];
    }
};
