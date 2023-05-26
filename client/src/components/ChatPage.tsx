import React, { useState } from 'react';
import axios from "axios";

const ChatPage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);

    // Create a new user message object with the input content and current timestamp
    const newUserMessage = {
      content: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric' })
    };

    // Update the messages state by appending the new user message
    setMessages(prevMessages => [...prevMessages, newUserMessage]);

    // Simulate API response
    sendRequest(inputMessage);

    // Clear the input field
    setInputMessage('');
  };

  const sendRequest = (input_message: string) => {
    axios.post('http://localhost:8000/chat', { input_message })
      .then(response => {
        console.log('Message sent:', response.data);
        const botResponse = {
          content: response.data.message,
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric' })
        };

        setMessages(prevMessages => [...prevMessages, botResponse]);
        setIsLoading(false);
      })
      .catch(error => {
        console.error('Error sending message:', error);
        setIsLoading(false);
      });
    };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputMessage(e.target.value);
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="container mx-auto py-4 px-6">
          <h1 className="text-2xl font-bold text-gray-800">Chat with OpenAI</h1>
        </div>
      </header>

      {/* Chat Container */}
      <div className="container mx-auto py-6 px-6">
        <div className="bg-white rounded-lg shadow-lg">
          {/* Chat Content */}
          <div className="h-64 overflow-y-auto px-4 py-2">
            <div className="flex flex-col space-y-2">
              {messages.map((message, index) => (
                <div
                  className={`flex ${
                    message.sender === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                  key={index}
                >
                  <div
                    className={`p-2 ${
                      message.sender === 'user' ? 'bg-blue-500' : 'bg-gray-200'
                    } rounded-lg`}
                  >
                    <p className={message.sender === 'user' ? 'text-white' : ''}>
                      {message.content}
                    </p>
                  </div>
                  <span className="text-xs text-gray-500 ml-2 self-end">
                    {message.timestamp}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Chat Input */}
          <div className="border-t border-gray-300 px-4 py-2">
            {isLoading && (
              <div className="text-center font-light italic mt-10 animate-pulse">
                Gimme a few seconds...
              </div>
            )}
            <form onSubmit={handleSubmit}>
              <input
                className="w-full rounded-lg py-2 px-4 border border-gray-300"
                type="text"
                placeholder="Type your message..."
                value={inputMessage}
                onChange={handleChange}
              />
              <button
                className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 mt-2 rounded-lg"
                type="submit"
              >
                Send
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
