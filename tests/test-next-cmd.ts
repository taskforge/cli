import { cli, generateTask, generateUser } from './utils';

describe('task next', () => {
    test('task next returns current task', async () => {
        const { token } = await generateUser();
        await generateTask(token);
        await generateTask(token);
        const currentTask = await generateTask(token, { priority: 2 });
        const { stdout } = await cli('next', token);
        const rgx = new RegExp(`^${currentTask.id} ${currentTask.title}`);
        expect(stdout).toMatch(rgx);
    });

    test('task next --title-only only prints current task title', async () => {
        const { token } = await generateUser();
        await generateTask(token);
        await generateTask(token);
        const currentTask = await generateTask(token, { priority: 2 });
        const { stdout } = await cli('next --title-only', token);
        const rgx = new RegExp(`^${currentTask.title}`);
        expect(stdout).toMatch(rgx);
    });

    test('task next --id-only only prints current task id', async () => {
        const { token } = await generateUser();
        await generateTask(token);
        await generateTask(token);
        const currentTask = await generateTask(token, { priority: 2 });
        const { stdout } = await cli('next --id-only', token);
        const rgx = new RegExp(`^${currentTask.id}`);
        expect(stdout).toMatch(rgx);
    });

    test('task next --json prints the current task as valid JSON', async () => {
        const { token } = await generateUser();
        await generateTask(token);
        await generateTask(token);
        const currentTask = await generateTask(token, { priority: 2 });
        const { stdout } = await cli('next --json', token);
        expect(JSON.parse(stdout)).toStrictEqual(currentTask);
    });
});
