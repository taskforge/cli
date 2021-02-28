import { cli, listTasks, generateTask, generateUser } from './utils';

describe('task complete', () => {
    test('no arguments completes the current task', async () => {
        const { token } = await generateUser();
        await generateTask(token);
        const { id } = await generateTask(token, { priority: 2 });
        await cli('complete', token);
        const tasks = await listTasks(token);
        for (const task of tasks) {
            if (task.id === id) {
                expect(task.completed_date).not.toBe(null);
            } else {
                expect(task.completed_date).toBe(null);
            }
        }
    });

    test('given an id completes the indicated task', async () => {
        const { token } = await generateUser();
        const { id } = await generateTask(token);
        await generateTask(token, { priority: 2 });
        await cli(`complete ${id}`, token);
        const tasks = await listTasks(token);
        for (const task of tasks) {
            if (task.id === id) {
                expect(task.completed_date).not.toBe(null);
            } else {
                expect(task.completed_date).toBe(null);
            }
        }
    });

    test('accepts multiple ids and completes the indicated tasks', async () => {
        const { token } = await generateUser();
        const { id } = await generateTask(token);
        const task2 = await generateTask(token, { priority: 2 });
        await cli(`complete ${id} ${task2.id}`, token);
        const tasks = await listTasks(token);
        for (const task of tasks) {
            expect(task.completed_date).not.toBe(null);
        }
    });

    test('done is an alias to complete', async () => {
        const { token } = await generateUser();
        await generateTask(token);
        const { id } = await generateTask(token, { priority: 2 });
        await cli('done', token);
        const tasks = await listTasks(token);
        for (const task of tasks) {
            if (task.id === id) {
                expect(task.completed_date).not.toBe(null);
            } else {
                expect(task.completed_date).toBe(null);
            }
        }
    });
});
