import axios from "axios";
import path from "path";
import { env } from "../config/env.js";

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

        console.error(error.response?.data || error.message);

        throw error;

    }
};