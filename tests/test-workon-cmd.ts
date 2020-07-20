import {
    cli,
    listTasks,
    generateTask,
    generateUser,
    getContextName
} from './utils';

describe('task workon', () => {
    test('given an id makes that task the highest priority task', async () => {
        const { token } = await generateUser();
        const { id } = await generateTask(token);
        await generateTask(token, { priority: 2 });
        await cli(`workon ${id}`, token);
        const tasks = await listTasks(token);
        for (const task of tasks) {
            if (task.id === id) {
                expect(task.priority).toBe(3);
            } else {
                expect(task.priority).toBe(2);
            }
        }
    });
});
