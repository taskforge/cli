import { isAPIError, tasks } from './client';
import { Command } from 'commander';

import { fail, unexpected } from './utils';
import { printList } from './printing';

async function list(args: string[], opts: Command) {
    try {
        const query = args.join(' ');
        let list;
        if (query !== '') {
            list = await tasks.search(query);
        } else {
            list = await tasks.list();
        }

        if (isAPIError(list)) {
            fail(list);
            return;
        }

        printList(list.data, opts.output);
    } catch (e) {
        unexpected(e);
    }
}

export const ListCommand = new Command('list')
    .alias('search')
    .alias('query')
    .alias('s')
    .alias('l')
    .alias('q')
    .description('list and search your tasks')
    .option(
        '-o --output <format>',
        'output format for the tasks, available formats: table, json, csv',
        'table'
    )
    .arguments('[query...]')
    .action(list);
