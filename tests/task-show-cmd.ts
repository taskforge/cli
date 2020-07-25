import { cli, generateTask, generateUser } from './utils';

describe('task show', () => {
    test('task show prints the given task', async () => {
        const { token } = await generateUser();
        const task = await generateTask(token);
        const { stdout } = await cli(`show ${task.id}`, token);
        expect(stdout).toMatch(
            new RegExp(
                `╔[═╤]*╗ *\n║ ID *│ ${task.id} *║ *\n╟─*┼─*╢ *\n║ Title *│ ${task.title} *║ *\n╟─*┼─*╢ *\n║ Priority *│ 1 *║ *\n╟─*┼─*╢ *\n║ Created Date *│ .* *║ *\n╟─*┼─*╢ *\n║ Completed Date │ null *║ *\n╟─*┼─*╢ *\n║ Source *│ Taskforge *║ *\n╟─*┼─*╢ *\n║ Context *│ default *║ *\n╟─*┼─*╢ *\n║ Owner *│ test-.*@example.com *║ *\n╚[═╧]*╝ *`
            )
        );
    });

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
