import { Command } from 'commander';

import { tasks, contexts, isAPIError } from '@taskforge/sdk';

import { fail, unexpected, highestPriority } from './utils';

async function getOrCreateContext(name: string): Promise<string> {
    const contextObj = await contexts.byName(name);
    if (!isAPIError(contextObj)) {
        return contextObj.id;
    }

    if (contextObj.code !== 404) {
        fail(contextObj);
        return '';
    }

    const createdContext = await contexts.create({ name });
    if (isAPIError(createdContext)) {
        fail(createdContext);
        return '';
    }

    return createdContext.id;
}

async function main() {
    const cli = new Command();
    cli.option('-t --top', 'if provided make this task the top priority')
        .option(
            '-c --context <name>',
            'the context in which to create the task',
            'default'
        )
        .arguments('[title...]')
        .parse(process.argv);

    const title = cli.args.join(' ');
    if (!title || title === '') {
        console.log('must provide a task title');
        process.exit(1);
    }

    let priority = 1;
    if (cli.top) {
        priority = (await highestPriority()) + 1;
    }

    try {
        let context;
        if (cli.context && cli.context !== 'default') {
            context = await getOrCreateContext(cli.context);
        }

        const response = await tasks.create({ title, priority, context });
        if (isAPIError(response)) {
            fail(response);
        }
    } catch (e) {
        unexpected(e);
    }
}

main();
