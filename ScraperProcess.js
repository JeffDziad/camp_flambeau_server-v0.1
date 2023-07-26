const {spawn} = require("child_process");

async function VrboReviewScraper(url) {
    return new Promise(resolve => {
        const python = spawn('python', ['./scripts/VrboReviewsScraper/main.py', url]);
        let output = {
            error: "No Data..."
        };
        python.stdout.on('data', function(data) {
            output = data.toString();
        });
        python.on('exit', function() {
            resolve(output);
        });
    });
}

module.exports = VrboReviewScraper;