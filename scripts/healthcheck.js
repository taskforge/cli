// eslint-disable-next-line
const fetch = require('node-fetch');

async function main() {
    const url = `${process.env.TASKFORGE_HOST}/v1/tasks`;
    const params = {
        method: 'OPTIONS'
    };

    let attempts = 0;
    while (attempts < 10) {
        console.log(`Attempt #${attempts} to connect to ${url}`);
        const response = await fetch(url, params);
        if (response.status === 200) {
            console.log('API is ready!');
            process.exit(0);
        }

        attempts++;
    }

    console.log(`Failed to connect after ${attempts} attempts.`);
    process.exit(1);
}

main();
