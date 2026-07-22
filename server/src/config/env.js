import dotenv from "dotenv";

dotenv.config();

const required = [
  "PORT",
  "MONGODB_URI",
  "PYTHON_SERVICE_URL"
];

for (const key of required) {
  if (!process.env[key]) {
    throw new Error(`Missing environment variable: ${key}`);
  }
}

export const env = {
  PORT: process.env.PORT,
  MONGODB_URI: process.env.MONGODB_URI,
  PYTHON_SERVICE_URL: process.env.PYTHON_SERVICE_URL
};