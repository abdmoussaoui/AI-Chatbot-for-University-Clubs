// src/services/chatApi.ts

// Interface pour correspondre à la structure de session attendue par le backend
interface SessionEntry {
  user_query: string;
  response: string;
  action: string;
}

// Interface pour la réponse du backend
export interface BotResponse {
  plot_url?: string | null;
  response: string;
  recommendation: {
    club: string;
    explanation: string;
    plot_url: string | null; // Permettre null pour gérer les cas où le plot échoue
  } | null;
  club_scores: { [key: string]: number } | null;
}

const API_BASE_URL = "http://localhost:8000";

/**
 * Sends a message and the entire conversation history to the backend.
 * @param message The new message from the user.
 * @param session The history of the conversation (array of objects).
 * @returns A promise that resolves to the complex BotResponse object.
 */
export const sendMessageToBot = async (
  message: string,
  session: SessionEntry[]
): Promise<BotResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // The body MUST match what our FastAPI backend expects
      body: JSON.stringify({
        message: message, // Utiliser "message" au lieu de "query"
        session: session, // Session est une liste de dictionnaires
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const errorMessage =
        errorData?.detail || `Request failed with status: ${response.status}`;
      throw new Error(errorMessage);
    }

    const data: BotResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Chat API Error:", error);
    throw error;
  }
};
