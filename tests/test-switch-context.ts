import {
    cli,
    genDir,
    generateTask,
    generateUser,
    createContext
} from './utils';

describe('task switch-context', () => {
    test('switches the context', async () => {
        const { token } = await generateUser();
        const so = { dataDir: genDir() };
        const context = await createContext(token, 'non-default');

        const expected = await generateTask(token, { context });
        const top = await generateTask(token, { priority: 2 });

        const verify = await cli('next', token, so);
        const rgx = new RegExp(`^${top.id} ${top.title}`);
        expect(verify.stdout).toMatch(rgx);

        await cli('switch-context non-default', token, so);
        const switched = await cli('next', token, so);
        const switchedRgx = new RegExp(`^${expected.id} ${expected.title}`);
        expect(switched.stdout).toMatch(switchedRgx);
    });

    test('resets the context', async () => {
        const { token } = await generateUser();
        const so = { dataDir: genDir() };
        const context = await createContext(token, 'non-default');

        const expected = await generateTask(token, { context });
        const top = await generateTask(token, { priority: 2 });

        const verify = await cli('next', token, so);
        const rgx = new RegExp(`^${top.id} ${top.title}`);
        expect(verify.stdout).toMatch(rgx);

        await cli('switch-context non-default', token, so);
        const switched = await cli('next', token, so);
        const switchedRgx = new RegExp(`^${expected.id} ${expected.title}`);
        expect(switched.stdout).toMatch(switchedRgx);

        await cli('switch-context --reset', token, so);
        const reset = await cli('next', token, so);
        const resetRgx = new RegExp(`^${top.id} ${top.title}`);
        expect(reset.stdout).toMatch(resetRgx);
    });
});
