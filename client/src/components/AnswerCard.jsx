function AnswerCard({ history }) {
  if (!history || history.length === 0) {
    return null;
  }

  return (
    <div className="answer-card">
      <h2>💬 Conversation</h2>

      {history.map((item, index) => (
        <div key={index} className="chat-message">
          <div className="user-message">
            <strong>🙋 You</strong>
            <p>{item.question}</p>
          </div>

          <div className="ai-message">
            <strong>🤖 AI</strong>
            <p>{item.answer}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default AnswerCard;