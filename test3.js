const scraper = require('amazon-buddy');

(async () => {
    try {
        // Collect 50 products from a keyword 'xbox one'
        // Default country is US
        const prod = await scraper.products({ keyword: 'condom', number: 1 ,country:'IN'});
        console.log(prod.result[0]['title']);
    } catch (error) {
        console.log(error);
    }
})();