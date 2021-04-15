import client from './client';
import { printList } from './printing';
import { unexpected } from './utils';
import { Command } from 'commander';

async function list(args: string[], opts: Command) {
    try {
        const query = args.join(' ');
        const list =
            query !== ''
                ? await client.tasks.search(query)
                : await client.tasks.list();
        await printList(list, opts.output);
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
