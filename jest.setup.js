jest.setTimeout(30000);
if (!process.env.TASKFORGE_HOST) {
    process.env.TASKFORGE_HOST = 'https://test.taskforge.io';
}

if (
    process.env.TASKFORGE_HOST == 'https://taskforge.io' ||
    process.env.TASKFORGE_HOST == 'http://taskforge.io'
) {
    throw new Error("Don't run the tests against production.");
}
