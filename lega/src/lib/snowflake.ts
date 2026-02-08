import snowflake from "snowflake-sdk";
import fs from "fs";
import path from "path";

// Load private key
function getPrivateKey() {
  if (process.env.SNOWFLAKE_PRIVATE_KEY_CONTENT) {
    return process.env.SNOWFLAKE_PRIVATE_KEY_CONTENT;
  }
  if (process.env.SNOWFLAKE_PRIVATE_KEY_PATH) {
    const keyPath = path.resolve(process.env.SNOWFLAKE_PRIVATE_KEY_PATH);
    if (fs.existsSync(keyPath)) {
      return fs.readFileSync(keyPath, "utf8");
    }
  }
  throw new Error("Snowflake private key not found in environment variables.");
}

const connection = snowflake.createConnection({
  account: process.env.SNOWFLAKE_ACCOUNT || "",
  username: process.env.SNOWFLAKE_USER || "",
  authenticator: "SNOWFLAKE_JWT",
  privateKey: getPrivateKey(),
  role: "SYSADMIN", // Or appropriate role
  warehouse: "COMPUTE_WH", // Default warehouse
  database: "LEGA_DB", // Default database
  schema: "PUBLIC", // Default schema
});

export async function executeQuery(
  sqlText: string,
  binds: any[] = [],
): Promise<any[]> {
  return new Promise((resolve, reject) => {
    connection.execute({
      sqlText,
      binds,
      complete: (err, _stmt, rows) => {
        if (err) {
          console.error("Snowflake execute error:", err);
          reject(err);
        } else {
          resolve(rows || []);
        }
      },
    });
  });
}

// Initial connection verification
connection.connect((err, _conn) => {
  if (err) {
    console.error("Unable to connect to Snowflake:", err.message);
  } else {
    console.log("Successfully connected to Snowflake.");
  }
});

export default connection;
