const VrboReviewScraper = require("./ScraperProcess");
const cron = require("node-cron");
const cors = require("cors");
const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const fsProm = require("fs/promises");
const jsonParser = bodyParser.json();
const app = express();
const port = 8080;
const LOYOLA_URL = "https://www.vrbo.com/2304851?noDates=true&unitId=2870995";
const MARQUETTE_URL = "https://www.vrbo.com/2137295?noDates=true&unitId=2701831";

app.use(cors());
app.use('/', express.static('live'));

app.post("/reviews", jsonParser, async (req, res) => {
    console.log("Request received...");
    let result = await readReviews();
    res.send(result);
});

async function updateReviews() {
    console.log("Updating reviews...");
    let loyola = await VrboReviewScraper(LOYOLA_URL);
    let marquette = await VrboReviewScraper(MARQUETTE_URL);
    fs.writeFile(__dirname + "/review_data/loyola_reviews.txt", loyola, err => {
        console.error(err);
    });
    fs.writeFile(__dirname + "/review_data/marquette_reviews.txt", marquette, err => {
        console.error(err);
    });
}

async function readReviews() {
    try {
        let loyola = await fsProm.readFile(__dirname + "/review_data/loyola_reviews.txt", {encoding: "utf8"});
        let marquette = await fsProm.readFile(__dirname + "/review_data/marquette_reviews.txt", {encoding: "utf8"});
        return {
            "Loyola": JSON.parse(loyola),// setViewableItems([reviewItems[0], reviewItems[1]]);
            "Marquette": JSON.parse(marquette)
        };
    } catch (err) {
        console.error(err);
    }
}

cron.schedule("0 * * * *", updateReviews);

app.listen(port, () => {
    updateReviews();
    console.log(`Listening on PORT ${port}...`)
});