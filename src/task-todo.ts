import { isAPIError, Task, tasks } from '@taskforge/sdk';
import { Command } from 'commander';

import { printList, fail } from './utils';

async function main() {
    const cli = new Command();
    cli.option(
        '-o --output <format>',
        'output format for the tasks, available formats: table, json, csv',
        'table'
    )
        .arguments('[query...]')
        .parse(process.argv);

    const list = await tasks.search('completed = false');
    if (isAPIError(list)) {
        fail(list);
        return;
    }

    printList(list, cli.output);
}

main();
