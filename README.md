# 📄 AI-Powered Document Q&A Service

An AI-powered application that allows users to upload PDF documents and ask questions about their content using Retrieval-Augmented Generation (RAG). The system extracts text from PDFs, converts it into vector embeddings, retrieves the most relevant information using ChromaDB, and generates accurate answers using Google's Gemini AI.

---

## 🚀 Features

- Upload PDF documents
- Extract text from PDFs
- Split documents into chunks
- Generate vector embeddings
- Store embeddings in ChromaDB
- Semantic search using embeddings
- AI-generated answers using Gemini
- Chat-style conversation history
- Modern React frontend
- REST APIs using Node.js and FastAPI

---

## 🛠 Tech Stack

### Frontend
- React.js
- Vite
- Axios
- CSS

### Backend
- Node.js
- Express.js
- MongoDB Atlas
- Multer

### AI Service
- FastAPI
- ChromaDB
- Sentence Transformers
- LangChain Text Splitter
- Google Gemini API

---

## 📂 Project Structure

```text
ai-document-qa-service/
│
├── client/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── App.css
│
├── server/
│   ├── src/
│   ├── uploads/
│   └── package.json
│
├── ai-service/
│   ├── app/
│   ├── chroma_db/
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository-url>
```

### Backend

```bash
cd server
npm install
npm run dev
```

### AI Service

```bash
cd ai-service

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Frontend

```bash
cd client

npm install

npm run dev
```

---

## 🔑 Environment Variables

### Server (.env)

```env
PORT=5000

MONGODB_URI=your_mongodb_connection_string

PYTHON_SERVICE_URL=http://localhost:8000
```

### AI Service (.env)

```env
GEMINI_API_KEY=your_gemini_api_key
```

---

## 📡 API Endpoints

### Upload PDF

```http
POST /api/upload
```

### Ask Question

```http
POST /api/ask
```

Request Body

```json
{
  "documentId": "...",
  "question": "What is this document about?"
}
```

---

## 🧠 How It Works

1. Upload a PDF document.
2. Node.js saves the file and metadata.
3. FastAPI extracts the text.
4. The text is divided into chunks.
5. Sentence Transformers generate embeddings.
6. ChromaDB stores the embeddings.
7. User asks a question.
8. ChromaDB retrieves the most relevant chunks.
9. Gemini generates the final answer.
10. React displays the response.

---

## 📷 Screenshots

Add screenshots of:

- Home Page
- Upload PDF
- Chat Interface
- AI Response

---

## 🔮 Future Improvements

- Multiple document support
- User authentication
- Drag-and-drop upload
- OCR for scanned PDFs
- Conversation memory
- Streaming AI responses

---

## 👨‍💻 Author

Pranay Rebeyro
