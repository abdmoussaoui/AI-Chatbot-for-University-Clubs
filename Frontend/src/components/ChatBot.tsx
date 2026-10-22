import { useEffect, useRef, useState } from 'react';
import { MessageCircle, RotateCcw, Sparkles } from 'lucide-react';
import { Message } from '../types/chat';
import { sendMessageToBot } from '../services/chatApi';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
const welcome = (): Message => ({ id: crypto.randomUUID(), text: 'Salut ! 👋 Moi, c’est ton guide des clubs FSBM. Parle-moi de ce que tu aimes, de tes envies ou de ce que tu aimerais découvrir. On trouvera ensemble le club qui te ressemble.', sender: 'bot', timestamp: new Date() });
export default function ChatBot() {
 const [messages, setMessages] = useState<Message[]>([welcome()]);
 const [session, setSession] = useState<{user_query: string; response: string; action: string}[]>([]);
 const [busy, setBusy] = useState(false);
 const [finished, setFinished] = useState(false);
 const [error, setError] = useState(false);
 const end = useRef<HTMLDivElement>(null);
 const lock = useRef(false);
 useEffect(() => { if (messages.length > 1 || busy) end.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }, [messages, busy]);
 const reset = () => { if (lock.current) return; setMessages([welcome()]); setSession([]); setFinished(false); setError(false); };
 const send = async (text: string) => {
  if (lock.current || finished || !text.trim()) return;
  lock.current = true; setBusy(true); setError(false);
  setMessages(p => [...p, { id: crypto.randomUUID(), text, sender: 'user', timestamp: new Date() }]);
  try {
   const data = await sendMessageToBot(text, session);
   setMessages(p => [...p, { id: crypto.randomUUID(), text: data.response, sender: 'bot', timestamp: new Date(), imageUrl: (data.plot_url || data.recommendation?.plot_url) ? `http://localhost:8000${data.plot_url || data.recommendation?.plot_url}` : undefined }]);
   setSession(p => [...p, {user_query: text, response: data.response, action: data.recommendation ? 'recommend' : 'ask'}]);
   setFinished(Boolean(data.recommendation));
  } catch { setError(true); } finally { lock.current = false; setBusy(false); }
 };
 return <main className="simple-page">
  <header className="page-header"><span className="logo"><MessageCircle size={27}/></span><h1>FSBM Club AI</h1><p>Trouvez le club qui correspond à vos passions et centres d’intérêt.</p></header>
  <section className="chat-panel" aria-label="Discussion avec l’assistant FSBM">
   <div className="chat-header"><span className="assistant-avatar"><Sparkles size={21}/></span><div><h2>Assistant FSBM</h2><p>{busy ? 'Réflexion en cours…' : finished ? 'Recommandation terminée' : 'Comment puis-je vous aider ?'}</p></div><button className="reset-button" onClick={reset} disabled={busy} aria-label="Nouvelle discussion" title="Nouvelle discussion"><RotateCcw size={18}/></button></div>
   <div className="chat-messages" role="log" aria-live="polite" aria-relevant="additions">{messages.map(m => <MessageBubble key={m.id} message={m}/>)}{busy && <p className="thinking">L’assistant écrit…</p>}<div ref={end}/></div>
   {error && <div className="error-notice" role="alert">Connexion impossible. Vérifiez que le serveur est lancé, puis réessayez.<button onClick={() => setError(false)} aria-label="Fermer">×</button></div>}
   {finished ? <div className="finished-bar"><span>Votre recommandation est prête.</span><button onClick={reset}>Nouvelle discussion</button></div> : <ChatInput onSendMessage={send} disabled={busy}/>}
  </section>
  <footer>Faculté des Sciences Ben M’Sik</footer>
 </main>;
}
