'use strict';
const { useState, useRef, useEffect } = React;
const { createRoot } = ReactDOM;

const ChatApp = () => {
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [threadId, setThreadId] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!inputText.trim()) return;

        setMessages(prev => [...prev, { type: 'user', content: inputText }]);
        setIsLoading(true);

        try {
            const response = await fetch('/api/v1/assistant', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: inputText,
                    ...(threadId && { thread_id: threadId }),
                }),
            });

            const data = await response.json();

            if (data.thread_id) {
                setThreadId(data.thread_id);
            }

            setMessages(prev => [...prev, { type: 'assistant', content: data.message }]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                type: 'error',
                content: 'Sorry, there was an error sending your message.'
            }]);
        } finally {
            setIsLoading(false);
            setInputText('');
        }
    };

    return React.createElement('div', {
        className: "flex flex-col h-screen max-w-3xl mx-auto p-4 bg-gray-50"
    }, [
        // Chat Window
        React.createElement('div', {
            key: 'chat-window',
            className: "flex-1 overflow-y-auto mb-4 bg-white rounded-lg shadow p-4"
        },
            React.createElement('div', {
                className: "space-y-4"
            }, [
                messages.map((message, index) =>
                    React.createElement('div', {
                        key: index,
                        className: `flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`
                    },
                        React.createElement('div', {
                            className: `max-w-[80%] px-4 py-2 rounded-lg ${
                                message.type === 'user'
                                    ? 'bg-blue-500 text-white rounded-br-none'
                                    : message.type === 'error'
                                    ? 'bg-red-100 text-red-700'
                                    : 'bg-gray-100 text-gray-800 rounded-bl-none'
                            }`
                        }, message.content)
                    )
                ),
                isLoading &&
                    React.createElement('div', {
                        key: 'loading',
                        className: "flex justify-start"
                    },
                        React.createElement('div', {
                            className: "bg-gray-100 text-gray-800 rounded-lg rounded-bl-none px-4 py-2"
                        },
                            React.createElement('div', {
                                className: "flex space-x-2"
                            }, [
                                React.createElement('div', {
                                    key: 'dot1',
                                    className: "w-2 h-2 bg-gray-400 rounded-full animate-bounce",
                                    style: { animationDelay: '0ms' }
                                }),
                                React.createElement('div', {
                                    key: 'dot2',
                                    className: "w-2 h-2 bg-gray-400 rounded-full animate-bounce",
                                    style: { animationDelay: '150ms' }
                                }),
                                React.createElement('div', {
                                    key: 'dot3',
                                    className: "w-2 h-2 bg-gray-400 rounded-full animate-bounce",
                                    style: { animationDelay: '300ms' }
                                })
                            ])
                        )
                    ),
                React.createElement('div', {
                    key: 'scroll-anchor',
                    ref: messagesEndRef
                })
            ])
        ),

        // Input Form
        React.createElement('form', {
            key: 'input-form',
            onSubmit: handleSubmit,
            className: "flex space-x-2"
        }, [
            React.createElement('input', {
                key: 'text-input',
                type: "text",
                value: inputText,
                onChange: (e) => setInputText(e.target.value),
                placeholder: "Type your message...",
                className: "flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            }),
            React.createElement('button', {
                key: 'submit-button',
                type: "submit",
                disabled: isLoading || !inputText.trim(),
                className: "px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed transition-colors duration-200 flex items-center"
            },
                // Create an SVG icon instead of using Lucide component
                React.createElement('svg', {
                    xmlns: "http://www.w3.org/2000/svg",
                    width: "20",
                    height: "20",
                    viewBox: "0 0 24 24",
                    fill: "none",
                    stroke: "currentColor",
                    strokeWidth: "2",
                    strokeLinecap: "round",
                    strokeLinejoin: "round"
                }, [
                    React.createElement('path', {
                        key: 'path1',
                        d: "M22 2L11 13"
                    }),
                    React.createElement('path', {
                        key: 'path2',
                        d: "M22 2L15 22L11 13L2 9L22 2"
                    })
                ])
            )
        ])
    ]);
};

// Mount the React application
const root = createRoot(document.getElementById('root'));
root.render(React.createElement(ChatApp));