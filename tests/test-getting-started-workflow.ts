import { cli, listTasks, generateUser, tableRegexp } from './utils';

const uuidRegex =
    '\\b[0-9a-f]{8}\\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\\b[0-9a-f]{12}\\b';

test('getting started guide works', async () => {
    const { email, token } = await generateUser();

    const addResult = await cli('add complete the Taskforge tutorial', token);
    expect(addResult.code).toBe(0);

    const listResult = await cli('list', token);
    expect(listResult.code).toBe(0);

    const tasks = await listTasks(token);
    expect(listResult.stdout).toMatch(tableRegexp(email, tasks));

    const nextResult = await cli('next', token);
    expect(nextResult.code).toBe(0);
    expect(nextResult.stdout).toMatch(
        new RegExp(`${uuidRegex} complete the Taskforge tutorial`)
    );

    const addResult2 = await cli('add another default priority task', token);
    expect(addResult2.code).toBe(0);
    const addResult3 = await cli(
        'add --priority 2 a high priority task',
        token
    );
    expect(addResult3.code).toBe(0);

    const multiPriorityTasks = await listTasks(token);

    const listResult2 = await cli('list', token);
    expect(listResult2.code).toBe(0);
    expect(listResult2.stdout).toMatch(tableRegexp(email, multiPriorityTasks));

    const nextResult2 = await cli('next', token);
    expect(nextResult2.code).toBe(0);
    expect(nextResult2.stdout).toMatch(
        new RegExp(`${uuidRegex} a high priority task`)
    );

    const completeId = multiPriorityTasks.filter(
        (t) => t.title === 'a high priority task'
    )[0].id;
    const completeResult = await cli(`complete ${completeId}`, token);
    expect(completeResult.code).toBe(0);

    const completeMultiPriorityTasks = await listTasks(token);
    const listResult3 = await cli('list', token);
    expect(listResult3.code).toBe(0);
    expect(listResult3.stdout).toMatch(
        tableRegexp(email, completeMultiPriorityTasks)
    );

    const queryList = await listTasks(token);
    const queryResult = await cli('query completed = false', token);
    expect(queryResult.code).toBe(0);
    expect(queryResult.stdout).toMatch(
        tableRegexp(
            email,
            queryList.filter((t) => t.completedDate === null)
        )
    );

    const todoResult = await cli('todo', token);
    expect(todoResult.code).toBe(0);
    expect(todoResult.stdout).toMatch(
        tableRegexp(
            email,
            completeMultiPriorityTasks.filter((t) => t.completedDate === null)
        )
    );

    const workonId = queryList.filter(
        (t) => t.title === 'another default priority task'
    )[0].id;
    const workonResult = await cli(`work-on ${workonId}`, token);
    expect(workonResult.code).toBe(0);

    const nextResult3 = await cli('next', token);
    expect(nextResult3.code).toBe(0);
    expect(nextResult3.stdout).toMatch(
        new RegExp(`${uuidRegex} another default priority task`)
    );

    const postCompleteList = await listTasks(token);
    const todoResult2 = await cli('todo', token);
    expect(todoResult2.code).toBe(0);
    expect(todoResult2.stdout).toMatch(
        tableRegexp(
            email,
            postCompleteList.filter((t) => t.completedDate === null)
        )
    );

    const completeResult2 = await cli('done', token);
    expect(completeResult2.code).toBe(0);

    const nextResult4 = await cli('next', token);
    expect(nextResult4.code).toBe(0);
    expect(nextResult4.stdout).toMatch(
        new RegExp(`${uuidRegex} complete the Taskforge tutorial`)
    );
});
