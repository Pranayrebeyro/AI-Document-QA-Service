import multer from "multer";
import path from "path";
import fs from "fs";

const uploadPath = "src/uploads";

// Create uploads folder if it doesn't exist
if (!fs.existsSync(uploadPath)) {
    fs.mkdirSync(uploadPath, { recursive: true });
}

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadPath);
    },

    filename: (req, file, cb) => {
        const uniqueName =
            Date.now() + "-" + file.originalname.replace(/\s+/g, "-");

        cb(null, uniqueName);
    },
});

const fileFilter = (req, file, cb) => {
    if (path.extname(file.originalname).toLowerCase() !== ".pdf") {
        return cb(new Error("Only PDF files are allowed."));
    }

    cb(null, true);
};

const upload = multer({
    storage,
    limits: {
        fileSize: 10 * 1024 * 1024,
    },
    fileFilter,
});

export default upload;