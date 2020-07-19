import {
    cli,
    listTasks,
    generateTask,
    generateUser,
    getContextName
} from './utils';

describe('task add', () => {
    test('task add creates task', async () => {
        const { ownerId, token } = await generateUser();
        await cli('add this is a test task', token);
        const taskList = await listTasks(token);
        expect(taskList.length).toBe(1);
        expect(taskList[0].title).toBe('this is a test task');
        expect(taskList[0].owner).toBe(ownerId);
        expect(taskList[0].priority).toBe(1);
    });

    test('task add --top makes the new task the highest priority task', async () => {
        const { ownerId, token } = await generateUser();
        const firstTask = await generateTask(token);
        await cli('add --top this is the new top priority', token);
        const taskList = await listTasks(token);
        expect(taskList.length).toBe(2);
        const createdTask = taskList.filter((t) => t.id !== firstTask.id)[0];
        expect(createdTask.title).toBe('this is the new top priority');
        expect(createdTask.owner).toBe(ownerId);
        expect(createdTask.priority).toBe(firstTask.priority + 1);
    });

    test('task add --context creates a task with the given context', async () => {
        const { ownerId, token } = await generateUser();
        await cli('add --context tests this is a test task', token);
        const taskList = await listTasks(token);
        expect(taskList.length).toBe(1);
        expect(taskList[0].title).toBe('this is a test task');
        expect(taskList[0].owner).toBe(ownerId);
        expect(await getContextName(token, taskList[0].context)).toBe('tests');
        expect(taskList[0].priority).toBe(1);
    });

    test('task add --priority creates a task with the given priority', async () => {
        const { ownerId, token } = await generateUser();
        await cli('add --priority 100 this is a test task', token);
        const taskList = await listTasks(token);
        expect(taskList.length).toBe(1);
        expect(taskList[0].title).toBe('this is a test task');
        expect(taskList[0].owner).toBe(ownerId);
        expect(taskList[0].priority).toBe(100);
    });
});
