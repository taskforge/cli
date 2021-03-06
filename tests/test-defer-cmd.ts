import { cli, listTasks, generateTask, generateUser } from './utils';

describe('task defer', () => {
    test('defers current task', async () => {
        const { token } = await generateUser();
        await generateTask(token);
        await generateTask(token, { priority: 2 });
        await cli('defer', token);
        const tasks = await listTasks(token);
        for (const task of tasks) {
            expect(task.priority).toBe(1);
        }
    });

    test('defers current task by making it the one less than lowest priority if priorities are equal', async () => {
        const { token } = await generateUser();
        const { id } = await generateTask(token);
        await generateTask(token);
        await generateTask(token);
        await cli('defer', token);
        const tasks = await listTasks(token);
        for (const task of tasks) {
            if (task.id === id) {
                expect(task.priority).toBe(0);
            } else {
                expect(task.priority).toBe(1);
            }
        }
    });
});
