import { Command } from 'commander';

import { tasks, contexts, isAPIError } from '@taskforge/sdk';

import { fail, unexpected, highestPriority } from './utils';

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
            const contextObj = await contexts.byName(cli.context);
            if (isAPIError(contextObj)) {
                fail(contextObj);
                return;
            }

            context = contextObj.id;
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
