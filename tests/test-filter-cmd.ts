import { cli, listFilters, generateTask, generateUser } from './utils';

describe('task filter', () => {
    test('filter save allows the creation of a filter', async () => {
        const { ownerId, token } = await generateUser();
        await cli('filter save test-filter completed = false', token);
        const filterList = await listFilters(token);
        expect(filterList.length).toBe(1);
        expect(filterList[0].name).toBe('test-filter');
        expect(filterList[0].owner).toBe(ownerId);
        expect(filterList[0].query).toBe('completed = false');
    });

    test('filter run runs the query', async () => {
        const { token } = await generateUser();
        await cli('filter save test-run-filter completed = false', token);
        const task1 = await generateTask(token);
        await generateTask(token, null, true);
        const expected = [task1];
        await generateTask(token, {}, true);
        const { stdout } = await cli(
            'filter run -o json test-run-filter',
            token
        );
        const parsed = JSON.parse(stdout);
        expect(parsed).toStrictEqual(expected);
    });

    test('filter update updates the query', async () => {
        const { token } = await generateUser();
        await cli('filter save test-update-filter completed = false', token);
        await cli('filter update test-update-filter completed = true', token);
        const filterList = await listFilters(token);
        expect(filterList[0].name).toBe('test-update-filter');
        expect(filterList[0].query).toBe('completed = true');
    });

    test('filter delete deletes the filter', async () => {
        const { token } = await generateUser();
        await cli('filter save test-delete-filter completed = false', token);
        const filterList = await listFilters(token);
        expect(filterList.length).toBe(1);
        await cli('filter delete test-delete-filter', token);
        const filterListAfter = await listFilters(token);
        expect(filterListAfter.length).toBe(0);
    });

    test('filter list lists available filter names', async () => {
        const { token } = await generateUser();
        await cli('filter save test-list-filter1 completed = true', token);
        await cli('filter save test-list-filter2 completed = true', token);
        const filterList = await listFilters(token);
        expect(filterList.length).toBe(2);
        const { stdout } = await cli('filter list', token);
        expect(stdout).toMatch(filterList.map((f) => f.name).join('\n'));
    });
});
