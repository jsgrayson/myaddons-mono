import { Message } from "../types";

const API_KEY = 'YOUR_GEMINI_API_KEY_HERE'; // Replace with actual key or env var
const API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';

export const sendMessage = async (msg: string): Promise<string> => {
    try {
        const response = await fetch(`${API_URL}?key=${API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `You are Lumina, an intelligent AI assistant embedded in a WoW-themed Holocron dashboard. Your responses should be concise, professional, and formatted with Markdown where appropriate. You are an expert in data analysis and business intelligence.\n\nUser: ${msg}`
                    }]
                }]
            })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;

        return text || "I couldn't generate a response. Please try again.";
    } catch (error) {
        console.error("Gemini API Error:", error);
        return "I'm having trouble connecting right now. Please check your API key and try again.";
    }
};
