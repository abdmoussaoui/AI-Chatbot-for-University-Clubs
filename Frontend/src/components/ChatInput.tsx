import { useState } from 'react';
import { ArrowUp, Sparkles } from 'lucide-react';
export default function ChatInput({ onSendMessage, disabled }: {onSendMessage: (message: string) => void; disabled?: boolean}) {
 const [message, setMessage] = useState('');
 const submit = () => { if (!disabled && message.trim()) { onSendMessage(message.trim()); setMessage(''); } };
 return <div className="composer-area"><form className="composer" onSubmit={e => { e.preventDefault(); submit(); }}><Sparkles className="composer-icon" size={19}/><textarea aria-label="Ton message" placeholder="Parle-moi de tes passions, de tes envies…" value={message} onChange={e => setMessage(e.target.value)} disabled={disabled} rows={1} onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); submit(); } }}/><button type="submit" aria-label="Envoyer le message" disabled={disabled || !message.trim()}><ArrowUp size={21}/></button></form><div className="composer-hint"><span>Sois toi-même, on s’occupe du reste.</span><span>Entrée pour envoyer ↵</span></div></div>;
}
