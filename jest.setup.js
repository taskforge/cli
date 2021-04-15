jest.setTimeout(30000);
if (!process.env.TASKFORGE_HOST) {
    process.env.TASKFORGE_HOST = 'https://api.test.taskforge.io/api';
}

if (
    process.env.TASKFORGE_HOST == 'https://taskforge.io' ||
    process.env.TASKFORGE_HOST == 'http://taskforge.io'
) {
    throw new Error("Don't run the tests against production.");
}

// Have to undefine this so Axios doesn't think jest tests are running in a browser. (It
// mocks this out somehow then we get CORs errors in the tests).
/* eslint-disable */
XMLHttpRequest = undefined;
