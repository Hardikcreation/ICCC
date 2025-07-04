import React from 'react';

const PostList = ({ posts }) => {
    return (
        <div className="space-y-6">
            <h3 className="text-2xl font-semibold text-gray-800 mb-4">Facebook Posts</h3>
            {posts.map(post => (
                <div
                    key={post.id}
                    className="border border-gray-200 rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
                >
                    <h4 className="text-lg font-medium text-gray-900 mb-2">
                        {post.message || 'No Message'}
                    </h4>

                    {post.image_url && (
                        <img
                            src={post.image_url}
                            alt="post"
                            className="max-w-xs rounded-md mb-3"
                        />
                    )}

                    <div className="flex flex-wrap gap-4 mb-3 text-sm">
                        <span className={`px-2 py-1 rounded-full ${post.sentiment === 'positive' ? 'bg-green-100 text-green-800' :
                                post.sentiment === 'negative' ? 'bg-red-100 text-red-800' :
                                    'bg-blue-100 text-blue-800'
                            }`}>
                            {post.sentiment}
                        </span>
                        <span className="text-gray-600">
                            <strong>Likes:</strong> {post.likes}
                        </span>
                        <span className="text-gray-600">
                            <strong>Shares:</strong> {post.shares}
                        </span>
                        <span className="text-gray-600">
                            <strong>Comments:</strong> {post.comments.length}
                        </span>
                    </div>

                    {post.comments.length > 0 && (
                        <div className="mt-4 border-t pt-4">
                            <h5 className="font-medium text-gray-700 mb-2">Comments:</h5>
                            <ul className="space-y-3">
                                {post.comments.map((c, idx) => (
                                    <li
                                        key={idx}
                                        className="p-3 bg-gray-50 rounded-md"
                                    >
                                        <p className="text-gray-800">{c.message}</p>
                                        <span className={`text-xs px-1.5 py-0.5 rounded ${c.sentiment === 'positive' ? 'bg-green-100 text-green-800' :
                                                c.sentiment === 'negative' ? 'bg-red-100 text-red-800' :
                                                    'bg-blue-100 text-blue-800'
                                            }`}>
                                            {c.sentiment}
                                        </span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
};

export default PostList;