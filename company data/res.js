let results = [];

async function fetchRestaurantData(link) {
  try {
    const response = await fetch(link);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    for (let item of data.results) {
      results.push(item);
    }
    console.log(`Fetched ${results.length} restaurants`);
    if (data.next) {
      await fetchRestaurantData(data.next);
    } else {
      console.log(JSON.stringify(results));

      const fs = require("fs");

      const jsonContent = JSON.stringify(results, null, 2);

      fs.writeFile("output.json", jsonContent, "utf8", (err) => {
        if (err) {
          console.error("Error writing to file:", err);
          return;
        }
        console.log("Data successfully written to output.json");
      });
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

fetchRestaurantData("https://www.gastronaut.hr/api/restoran/");
