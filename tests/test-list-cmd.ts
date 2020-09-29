import { cli, generateTask, generateUser } from './utils';

describe('task list', () => {
    test('--output json returns valid json', async () => {
        const { token } = await generateUser();
        const task = await generateTask(token);
        const { stdout } = await cli('list -o json', token);
        const parsed = JSON.parse(stdout);
        expect(parsed).toStrictEqual([task]);
    });

    test('lists all tasks', async () => {
        const { token } = await generateUser();
        const task1 = await generateTask(token);
        const task2 = await generateTask(token);
        const task3 = await generateTask(token, {}, true);
        const { stdout } = await cli('list -o json', token);
        const parsed = JSON.parse(stdout);
        expect(parsed).toStrictEqual([task1, task2, task3]);
    });

    test('list accepts TQL queries', async () => {
        const { token } = await generateUser();
        const task1 = await generateTask(token);
        await generateTask(token, null, true);
        const expected = [task1];
        await generateTask(token, {}, true);
        const { stdout } = await cli('list -o json completed = false', token);
        const parsed = JSON.parse(stdout);
        expect(parsed).toStrictEqual(expected);
    });

    test('todo is an alias for list completed = false', async () => {
        const { token } = await generateUser();
        const task1 = await generateTask(token);
        await generateTask(token, null, true);
        const expected = [task1];
        await generateTask(token, {}, true);
        const { stdout } = await cli('todo -o json', token);
        const parsed = JSON.parse(stdout);
        expect(parsed).toStrictEqual(expected);
    });

    test.each(['q', 'query', 'l'])('%s is an alias for list', async (alias) => {
        const { token } = await generateUser();
        const task = await generateTask(token);
        const { stdout } = await cli(`${alias} -o json`, token);
        const parsed = JSON.parse(stdout);
        expect(parsed).toStrictEqual([task]);
    });
});
