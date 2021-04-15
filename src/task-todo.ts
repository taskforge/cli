import client from './client';
import { printList } from './printing';
import { unexpected } from './utils';
import { Command } from 'commander';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
async function todo(opts: Command) {
    try {
        const list = await client.tasks.search('completed = false');
        printList(list, opts.output);
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
