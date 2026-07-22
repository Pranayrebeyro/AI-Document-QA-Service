import axios from "axios";
import { env } from "../config/env.js";

export const askQuestion = async (req, res) => {
    try {
        const { question, documentId } = req.body;

        if (!question || !documentId) {
            return res.status(400).json({
                success: false,
                message: "Question and documentId are required."
            });
        }

        const response = await axios.post(
            `${env.PYTHON_SERVICE_URL}/ask`,
            {
                question,
                documentId
            }
        );

        return res.json(response.data);

    } catch (error) {
        console.error(error);

        return res.status(500).json({
            success: false,
            message: error.message
        });
    }
};