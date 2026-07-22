import { useState } from "react";
import "./App.css";

import UploadForm from "./components/UploadForm";
import QuestionForm from "./components/QuestionForm";
import AnswerCard from "./components/AnswerCard";

function App() {
  const [documentId, setDocumentId] = useState("");
  const [history, setHistory] = useState([]);

  return (
    <div className="container">
      <header>
        <h1>📄 AI Document Q&A Service</h1>
        <p>Upload a PDF and chat with your document using AI.</p>
      </header>

      <div className="card">
        <UploadForm
          setDocumentId={setDocumentId}
          setHistory={setHistory}
        />
      </div>

      {documentId && (
        <>
          <div className="status-card">
            <h3>✅ Document Ready</h3>

            <p>
              <strong>Document ID</strong>
            </p>

            <div className="document-id">
              {documentId}
            </div>
          </div>

          <div className="card">
            <QuestionForm
              documentId={documentId}
              history={history}
              setHistory={setHistory}
            />
          </div>

          <AnswerCard history={history} />
        </>
      )}
    </div>
  );
}

export default App;