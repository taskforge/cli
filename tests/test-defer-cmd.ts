import { cli, listTasks, generateTask, generateUser } from './utils';

describe('task defer', () => {
    test('given an id makes that task the highest priority task', async () => {
        const { token } = await generateUser();
        await generateTask(token);
        await generateTask(token, { priority: 2 });
        await cli('defer', token);
        const tasks = await listTasks(token);
        for (const task of tasks) {
            expect(task.priority).toBe(1);
        }
    });
});
