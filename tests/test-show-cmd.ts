import { cli, generateTask, generateUser } from './utils';

describe('task show', () => {
    test('task show --output title only prints task title', async () => {
        const { token } = await generateUser();
        const task = await generateTask(token);
        const { stdout } = await cli(`show --output title ${task.id}`, token);
        const rgx = new RegExp(`^${task.title}`);
        expect(stdout).toMatch(rgx);
    });

    test('task show --output json prints the task as valid JSON', async () => {
        const { token } = await generateUser();
        const task = await generateTask(token);
        const { stdout } = await cli(`show --output json ${task.id}`, token);
        expect(JSON.parse(stdout)).toStrictEqual({ comments: [], ...task });
    });
});
