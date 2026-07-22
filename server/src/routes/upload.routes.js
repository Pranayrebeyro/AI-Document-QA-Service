import express from "express";

import upload from "../middleware/upload.middleware.js";

import { uploadDocument } from "../controllers/upload.controller.js";

const router = express.Router();

router.post(
    "/",
    upload.single("pdf"),
    uploadDocument
);

export default router;