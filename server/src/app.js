import express from "express";
import cors from "cors";
import morgan from "morgan";

import uploadRoutes from "./routes/upload.routes.js";
import questionRoutes from "./routes/question.routes.js";

const app = express();

app.use(cors());
app.use(express.json());
app.use(morgan("dev"));

app.get("/health", (req, res) => {
    res.json({
        success: true,
        message: "Server Running 🚀",
    });
});

app.use("/api/upload", uploadRoutes);
app.use("/api/ask", questionRoutes);

export default app;