import { useState } from "react";
import api from "../services/api";

function UploadForm({ setDocumentId, setHistory }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [fileName, setFileName] = useState("");

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
      setMessage("");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("❌ Please select a PDF file.");
      return;
    }

    const formData = new FormData();
    formData.append("pdf", file);

    try {
      setLoading(true);
      setMessage("");

      const response = await api.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log(response.data);

      // Ensure the response contains the document ID
      if (
        response.data &&
        response.data.document &&
        response.data.document._id
      ) {
        setDocumentId(response.data.document._id);
      } else {
        throw new Error("Document ID not found in response.");
      }

      // Clear previous conversation
      setHistory([]);

      setMessage("✅ PDF uploaded successfully.");

    } catch (error) {
      console.error(error);
      setMessage("❌ Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>📄 Upload PDF</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
      />

      {fileName && (
        <p>
          <strong>Selected File:</strong> {fileName}
        </p>
      )}

      <br />

      <button
        onClick={handleUpload}
        disabled={loading}
      >
        {loading ? "Uploading..." : "Upload PDF"}
      </button>

      {message && (
        <p className={message.startsWith("✅") ? "success" : "error"}>
          {message}
        </p>
      )}
    </div>
  );
}

export default UploadForm;