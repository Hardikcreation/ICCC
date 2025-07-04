// src/pages/Facebook.jsx
import React, { useEffect, useState } from "react";
import { fetchFacebookPosts } from "../services/api";
import SentimentChart from "../components/SentimentChart";
import CommentsChart from "../components/CommentsChart";
import PostList from "../components/PostList";

const Facebook = () => {
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        fetchFacebookPosts().then(setPosts);
    }, []);

    return (
        <div className="container mx-auto px-4 py-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">Facebook Sentiment Analysis</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <CommentsChart posts={posts} />
                </div>
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <SentimentChart posts={posts} />
                </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
                <PostList posts={posts} />
            </div>
        </div>
    );
};

export default Facebook;