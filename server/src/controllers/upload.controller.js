import Document from "../models/document.model.js";
import { processDocument } from "../services/python.service.js";

export const uploadDocument = async (req, res) => {

    try {

        if (!req.file) {

            return res.status(400).json({
                success: false,
                message: "No PDF uploaded."
            });

        }

        const document = await Document.create({

            originalName: req.file.originalname,
            fileName: req.file.filename,
            filePath: req.file.path,
            fileSize: req.file.size,
            status: "processing"

        });

        await processDocument(document);

        document.status = "completed";

        await document.save();

        return res.status(201).json({

            success: true,
            document

        });

    } catch (error) {

        console.error(error);

        return res.status(500).json({

            success: false,
            message: error.message

        });

    }

};