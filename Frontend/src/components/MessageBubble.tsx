import { Sparkles } from 'lucide-react';
import { Message } from '../types/chat';
export default function MessageBubble({ message }: { message: Message }) {
 const bot = message.sender === 'bot';
 return <div className={`message-row ${bot ? 'bot-message' : 'user-message'}`}>
  {bot && <span className="message-avatar"><Sparkles size={17}/></span>}
  <div className="message-content"><span className="message-author">{bot ? 'Assistant FSBM' : 'Toi'} <time>{message.timestamp.toLocaleTimeString('fr-FR', {hour: '2-digit', minute: '2-digit'})}</time></span><div className="message-bubble"><p>{message.text}</p>{message.imageUrl && <a href={message.imageUrl} target="_blank" rel="noreferrer"><img src={message.imageUrl} alt="Graphique de compatibilité avec les clubs FSBM"/></a>}</div></div>
 </div>;
}

