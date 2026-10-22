export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  isTyping?: boolean;
  isError?: boolean;
  imageUrl?: string;
}

export interface ChatState {
  messages: Message[];
  isTyping: boolean;
}
