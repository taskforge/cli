import { isAPIError, tasks } from './client';
import { Command } from 'commander';

import { fail, unexpected } from './utils';
import { printList } from './printing';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
async function todo(opts: Command) {
    try {
        const list = await tasks.search('completed = false');
        if (isAPIError(list)) {
            fail(list);
            return;
        }

        printList(list.results, opts.output);
    } catch (e) {
        unexpected(e);
    }
}

export const TodoCommand = new Command('todo')
    .alias('td')
    .description('list your incomplete tasks')
    .option(
        '-o --output <format>',
        'output format for the tasks, available formats: table, json, csv',
        'table'
    )
    .action(todo);
