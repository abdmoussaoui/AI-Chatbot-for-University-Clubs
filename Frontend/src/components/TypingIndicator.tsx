import React from 'react';
import { Bot, Sparkles } from 'lucide-react';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex items-start gap-4 mb-6 animate-fadeInUp">
      <div className="flex-shrink-0 relative">
        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg">
          <Bot size={20} className="text-white" />
        </div>
        <div className="absolute -top-1 -right-1 w-5 h-5 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center animate-pulse">
          <Sparkles size={10} className="text-white" />
        </div>
      </div>
      
      <div className="bg-white/90 backdrop-blur-sm border border-slate-200 px-6 py-4 rounded-2xl shadow-lg">
        <div className="flex items-center space-x-2">
          <div className="flex space-x-1">
            <div className="w-2.5 h-2.5 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full animate-bounce"></div>
            <div className="w-2.5 h-2.5 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2.5 h-2.5 bg-gradient-to-r from-indigo-500 to-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
          <span className="text-sm text-slate-600 font-medium ml-2">AI is thinking...</span>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;