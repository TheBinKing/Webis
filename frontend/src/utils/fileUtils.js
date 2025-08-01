import fs from "fs";
import path from "path";

export const readFile = async (filePath) => {
  try {
    const absolutePath = path.resolve(process.cwd(), filePath);
    return await fs.promises.readFile(absolutePath, "utf8");
  } catch (error) {
    console.error("读取文件失败:", error);
    throw error;
  }
};

export const writeFile = async (filePath, data) => {
  try {
    const absolutePath = path.resolve(process.cwd(), filePath);
    await fs.promises.writeFile(absolutePath, data, "utf8");
  } catch (error) {
    console.error("写入文件失败:", error);
    throw error;
  }
};
