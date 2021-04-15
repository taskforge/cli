import client from './client';
import { unexpected, highestPriority } from './utils';
import { Command } from 'commander';

async function getOrCreateContext(name: string): Promise<string> {
    try {
        const contextObj = await client.contexts.byName(name);
        return contextObj.id;
    } catch (e) {
        const createdContext = await client.contexts.create({ name });
        return createdContext.id;
    }
}

async function add(args: string[], opts: Command) {
    const title = args.join(' ');
    if (!title || title === '') {
        console.error('must provide a task title');
        process.exit(2);
    }

    let priority: number;
    try {
        priority = parseInt(opts.priority, 10);
    } catch (e) {
        console.error(
            `Unable to parse priority: ${opts.priority}, make sure it's a valid integer.`
        );
        process.exit(3);
    }

    if (opts.top) {
        priority = (await highestPriority()) + 1;
    }

    try {
        let context;
        if (opts.context && opts.context !== 'default') {
            context = await getOrCreateContext(opts.context);
        }

        await client.tasks.create({ title, priority, context });
    } catch (e) {
        unexpected(e);
    }
}

export const AddCommand = new Command('add')
    .alias('a')
    .alias('new')
    .description('add a task to your list')
    .arguments('[title...]')
    .option('-t --top', 'if provided make this task the top priority')
    .option(
        '-c --context <name>',
        'the context in which to create the task',
        'default'
    )
    .option(
        '-p --priority <priority>',
        'Explicitly set the priority of the task, ignored if --top provided',
        '1'
    )
    .action(add);
