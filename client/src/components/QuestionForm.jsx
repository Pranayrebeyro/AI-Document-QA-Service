import { useState } from "react";
import api from "../services/api";

function QuestionForm({ documentId, history, setHistory }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAsk = async () => {
    if (!question.trim()) {
      setError("❌ Please enter a question.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const response = await api.post("/ask", {
        documentId,
        question,
      });

      if (response.data.success) {
        setHistory((prevHistory) => [
          ...prevHistory,
          {
            question,
            answer: response.data.answer,
          },
        ]);

        setQuestion("");
      } else {
        setError(response.data.message || "No answer found.");
      }
    } catch (err) {
      console.error(err);
      setError("❌ Failed to generate answer.");
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setHistory([]);
    setQuestion("");
    setError("");
  };

  return (
    <div>
      <h2>💬 Ask Questions</h2>

      <input
        className="question-input"
        type="text"
        placeholder="Ask anything about your uploaded PDF..."
        value={question}
        disabled={!documentId}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleAsk();
          }
        }}
      />

      <div className="button-group">
        <button
          onClick={handleAsk}
          disabled={loading || !documentId}
        >
          {loading ? "Generating..." : "Ask"}
        </button>

        <button
          className="secondary-btn"
          onClick={clearChat}
          disabled={loading}
        >
          Clear Chat
        </button>
      </div>

      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default QuestionForm;