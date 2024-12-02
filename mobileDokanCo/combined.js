const fs = require("fs");
const path = require("path");

// Directory containing your JSON files
const directoryPath = path.join(__dirname, "separated");
const outputFilePath = path.join(__dirname, "combined.json");

// Initialize an empty array to hold the combined data
let combinedData = [];

// Read all files in the directory
fs.readdir(directoryPath, (err, files) => {
  if (err) {
    return console.error("Could not list the directory.", err);
  }

  files.forEach((file) => {
    const filePath = path.join(directoryPath, file);
    const fileData = JSON.parse(fs.readFileSync(filePath, "utf-8"));

    // Ensure each JSON file has an array structure and concatenate
    if (Array.isArray(fileData)) {
      combinedData = combinedData.concat(fileData);
    } else {
      console.warn(`${file} is not an array and was skipped.`);
    }
  });

  // Write the combined data to a new JSON file
  fs.writeFileSync(outputFilePath, JSON.stringify(combinedData, null, 2));
  console.log("All JSON files have been combined into combined.json");
});
