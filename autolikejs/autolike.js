const { Builder, By, Key, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const logging = require('selenium-webdriver/lib/logging');

const lastPost = 723;

usernamePasswords = [
    {
        "username": "tahmidAhmed",
        "password": "q1w2e3r4",
    },
    {
        "username": "SajidIslam",
        "password": "q1w2e3r4",
    },
    {
        "username": "MehediHasan",
        "password": "q1w2e3r4",
    },
    {
        "username": "FarhanIslam",
        "password": "q1w2e3r4",
    },
    {
        "username": "RafsanMahmud",
        "password": "q1w2e3r4",
    },
    {
        "username": "TanvirAlam",
        "password": "q1w2e3r4",
    },
    {
        "username": "ZareenFarhana",
        "password": "q1w2e3r4",
    },
    {
        "username": "AyanChowdhury",
        "password": "q1w2e3r4",
    },
    {
        "username": "aaaaa",
        "password": "aaaaaa",
    },
    {
        "username": "bbbbb",
        "password": "bbbbbb",
    },
    {
        "username": "ccccc",
        "password": "cccccc",
    },
    {
        "username": "ddddd",
        "password": "dddddd",
    },
    {
        "username": "eeeee",
        "password": "eeeeee",
    },
    {
        "username": "fffff",
        "password": "ffffff",
    },
    {
        "username": "ggggg",
        "password": "gggggg",
    },
    {
        "username": "hhhhh",
        "password": "hhhhhh",
    },
    {
        "username": "iiiii",
        "password": "iiiiii",
    },
    {
        "username": "jjjjj",
        "password": "jjjjjj",
    },
    {"username": "AyeshaRahman", "password": "q1w2e3r4"},
    {"username": "ImranHossain", "password": "q1w2e3r4"},
    {"username": "ZaraAhmed", "password": "q1w2e3r4"},
    {"username": "TariqAnwar", "password": "q1w2e3r4"},
    {"username": "NadiaKarim", "password": "q1w2e3r4"},
    {"username": "ArifChowdhury", "password": "q1w2e3r4"},
    {"username": "SabinaSultana", "password": "q1w2e3r4"},
    {"username": "FarhanMahmud", "password": "q1w2e3r4"},
    {"username": "MehnazIslam", "password": "q1w2e3r4"},
    {"username": "RinaBegum", "password": "q1w2e3r4", "gender": "female"},
    {"username": "AnisurRahman", "password": "q1w2e3r4", "gender": "male"},
    {"username": "ShakilAhmed", "password": "q1w2e3r4", "gender": "male"},
    {"username": "RahulChowdhury", "password": "q1w2e3r4", "gender": "male"},
    {"username": "SaraKhan", "password": "q1w2e3r4", "gender": "female"},
    {"username": "AmitSingh", "password": "q1w2e3r4", "gender": "male"},
    {"username": "NinaJain", "password": "q1w2e3r4", "gender": "female"},
    {
        "username": "ShafiqRahman",
        "password": "q1w2e3r4",
    },
    {
        "username": "RaheelSiddiqui",
        "password": "q1w2e3r4",
    },
    {
        "username": "NusratJahan",
        "password": "q1w2e3r4",
    },
    {
        "username": "OmarFaruq",
        "password": "q1w2e3r4",
    },
    {
        "username": "TamannaAkter",
        "password": "q1w2e3r4",
    },
    {
        "username": "FahimHasan",
        "password": "q1w2e3r4",
    },
    {
        "username": "LailaNoor",
        "password": "q1w2e3r4",
    },
    {
        "username": "JamilKhan",
        "password": "q1w2e3r4",
    },
    {"username": "RaviPatel", "password": "q1w2e3r4", "gender": "male"},
    {"username": "PoojaVerma", "password": "q1w2e3r4", "gender": "female"},
    {"username": "VikramSharma", "password": "q1w2e3r4", "gender": "male"},
    {"username": "AnitaDesai", "password": "q1w2e3r4", "gender": "female"},
    {"username": "MahmudHassan", "password": "q1w2e3r4", "gender": "male"},
    {"username": "ShabnamAkter", "password": "q1w2e3r4", "gender": "female"},
    {"username": "NafisAhmed", "password": "q1w2e3r4", "gender": "male"},
    {"username": "TaslimaBegum", "password": "q1w2e3r4", "gender": "female"},
    {"username": "RakibulIslam", "password": "q1w2e3r4", "gender": "male"},
    {"username": "SumaiyaJahan", "password": "q1w2e3r4", "gender": "female"},
    {"username": "FahimRahman", "password": "q1w2e3r4", "gender": "male"},
    {"username": "MalihaIslam", "password": "q1w2e3r4", "gender": "female"},
    {"username": "RashedKhan", "password": "q1w2e3r4", "gender": "male"},
    {"username": "SadiaRahman", "password": "q1w2e3r4", "gender": "female"},
    {"username": "AlaminMiah", "password": "q1w2e3r4", "gender": "male"},
    {"username": "FarzanaAkter", "password": "q1w2e3r4", "gender": "female"},
    {"username": "ShahinAlam", "password": "q1w2e3r4", "gender": "male"},
    {"username": "RubinaSultana", "password": "q1w2e3r4", "gender": "female"},
    {"username": "FerdousAhmed", "password": "q1w2e3r4", "gender": "male"},
    {"username": "MarufaIslam", "password": "q1w2e3r4", "gender": "female"},
    {"username": "AsifIqbal", "password": "q1w2e3r4", "gender": "male"},
    {"username": "LamiaKhanum", "password": "q1w2e3r4", "gender": "female"},
    {"username": "TamimKhan", "password": "q1w2e3r4", "gender": "male"},
    {"username": "MasudRahman", "password": "q1w2e3r4", "gender": "male"},
    {"username": "Hasanuzzaman", "password": "q1w2e3r4", "gender": "male"},
    {"username": "HamzaChowdhory", "password": "q1w2e3r4", "gender": "male"},
    {"username": "TowhidHridoy", "password": "q1w2e3r4", "gender": "male"},
]

async function autoLike(username, password, lastPost) {
    console.log(`Attempting to post for user: ${username}`);

    // Setting up Chrome options
    const options = new chrome.Options();
    options.addArguments('--headless'); // Run in headless mode
    options.addArguments('--disable-gpu');
    options.addArguments('--no-sandbox');
    options.addArguments('--disable-dev-shm-usage');

    let driver = await new Builder()
        .forBrowser('chrome')
        .setChromeOptions(options)
        .build();

    try {
        await driver.get('https://www.barlix.com/logout/');
        await driver.get('https://www.barlix.com/welcome/');

        // Logging in
        await driver.findElement(By.id('username')).sendKeys(username);
        await driver.findElement(By.id('password')).sendKeys(password);
        await driver.findElement(By.xpath('//button[@type="submit" and text()="Login"]')).click();

        await driver.wait(until.elementLocated(By.xpath('//textarea[@name="postText"]')), 20000);

        let processedPosts = [];
        let stop = false;
        const SCROLL_PAUSE_TIME = 5000;

        while (!stop) {
            let elements = await driver.findElements(By.xpath('//ul[@style=" right: auto; "]'));

            for (let box of elements) {
                let postId = await box.getAttribute("data-id");

                // Ignore specific posts
                const ignore = [
                    `${lastPost + 3}`, `${lastPost + 7}`, `${lastPost + 9}`,
                    `${lastPost + 13}`, `${lastPost + 16}`, `${lastPost + 20}`
                ];

                if (Math.floor(Math.random() * 5) === 2 && !ignore.includes(postId)) {
                    console.log(`${postId} -> Post is not liked.`);
                    continue;
                }

                try {
                    const reacts = await box.findElements(By.xpath('.//li'));
                    const index = [0, 1, 0, 1, 3, 0, 1, 3, 0, 1, 3, 4];
                    const rand = Math.floor(Math.random() * 12);
                    const element = reacts[index[rand]];

                    await driver.executeScript('arguments[0].scrollIntoView(true);', box);
                    await driver.executeScript('arguments[0].click();', element);

                    processedPosts.push(postId);
                    console.log(`${postId} -> Post liked successfully.`);
                } catch (err) {
                    console.log(`Failed to like post: ${postId}`);
                }

                if (parseInt(postId) <= lastPost) {
                    stop = true;
                    break;
                }
            }

            await driver.executeScript('window.scrollTo(0, document.body.scrollHeight);');
            await driver.sleep(SCROLL_PAUSE_TIME);
        }
    } finally {
        console.log('Auto-like process completed.');
        await driver.quit();
    }
}

async function run() {
    for (let user of usernamePasswords) {
        await autoLike(user.username, user.password, lastPost);
    }
}

run().catch(console.error);





// let limit = 5;

// for (let loop = 0; loop < Math.ceil(usernamePasswords.length / limit); loop++) {
//     let start = loop * limit;
//     let end = start + limit;
//     let users = usernamePasswords.slice(start, end);

//     try {
//         const tasks = users.map(user => autoLike(user.username, user.password, lastPost));
//         await Promise.all(tasks);
//         console.log(`Batch ${loop + 1} completed successfully.`);
//     } catch (error) {
//         console.error(`Error in batch ${loop + 1}:`, error.message);
//     }
// }

// console.log('All users have completed their tasks.');