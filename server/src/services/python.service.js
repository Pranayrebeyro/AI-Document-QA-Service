import axios from "axios";
import path from "path";
import { env } from "../config/env.js";

// -------------------------
// Process PDF
// -------------------------

export const processDocument = async (document) => {
    try {
        const absolutePath = path.resolve(document.filePath);

        const response = await axios.post(
            `${env.PYTHON_SERVICE_URL}/process`,
            {
                documentId: document._id.toString(),
                pdfPath: absolutePath,
            }
        );

        return response.data;

    } catch (error) {

        console.error("Process Error:");
        console.error(error.response?.data || error.message);

        throw error;
    }
};

// -------------------------
// Ask Question
// -------------------------

export const askQuestion = async (documentId, question) => {
    try {

        const response = await axios.post(
            `${env.PYTHON_SERVICE_URL}/ask`,
            {
                documentId,
                question,
            }
        );

        console.log("Python Response:");
        console.log(response.data);

        return response.data;

    } catch (error) {

        console.error("Ask Error:");
        console.error(error.response?.data || error.message);

        throw error;
    }
};