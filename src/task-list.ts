import { isAPIError, Task, tasks } from '@taskforge/sdk';
import { Command } from 'commander';

import { fail } from './utils';
import { printList } from './printing';

async function main() {
    const cli = new Command();
    cli.option(
        '-o --output <format>',
        'output format for the tasks, available formats: table, json, csv',
        'table'
    )
        .arguments('[query...]')
        .parse(process.argv);

    const query = cli.args.join(' ');
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

    printList(list, cli.output);
}

main();
