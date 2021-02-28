import { Command } from 'commander';

import { filters, tasks, isAPIError } from './client';

import { fail } from './utils';
import { printList } from './printing';

async function save(name: string, query: string[]): Promise<void> {
    const joined = query.join(' ');
    if (!joined || joined == '') {
        console.log('Must provide a query!');
        process.exit(1);
    }

    const saved = await filters.create({
        name,
        query: joined
    });
    if (isAPIError(saved)) {
        fail(saved);
    }
}

async function update(name: string, query: string[]): Promise<void> {
    const joined = query.join(' ');
    if (!joined || joined == '') {
        console.log('Must provide a query!');
        process.exit(1);
    }

    const filter = await filters.byName(name);
    if (isAPIError(filter)) {
        fail(filter);
        return;
    }

    const updated = await filters.update({
        ...filter,
        query: joined
    });
    if (isAPIError(updated)) {
        fail(updated);
    }
}

async function del(name: string): Promise<void> {
    const filter = await filters.byName(name);
    if (isAPIError(filter)) {
        fail(filter);
        return;
    }

    const deleted = await filters.del(filter.id);
    if (isAPIError(deleted)) {
        fail(deleted);
    }
}

async function run(name: string, opts: Command): Promise<void> {
    const filter = await filters.byName(name);
    if (isAPIError(filter)) {
        fail(filter);
        return;
    }

    const list = await tasks.search(filter.query);
    if (isAPIError(list)) {
        fail(list);
        return;
    }

    printList(list.results, opts.output);
}

async function list(opts: Command): Promise<void> {
    const list = await filters.list();
    if (isAPIError(list)) {
        fail(list);
        return;
    }

    for (const f of list.results) {
        if (opts.verbose) {
            console.log(f.name, f.query);
        } else {
            console.log(f.name);
        }
    }
}

const saveCommand = new Command('save')
    .description('save query as name for later use')
    .arguments('<name> [query...]')
    .action(save);

const updateCommand = new Command('update')
    .description('update the filter name with the new query')
    .arguments('update <name> [query...]')
    .action(update);

const deleteCommand = new Command('delete')
    .description('delete the given query')
    .arguments('delete <name>')
    .action(del);

const listCommand = new Command('list')
    .description('list your saved filters')
    .option(
        '-v --verbose',
        'print the associated query as well as the name of the filter',
        false
    )
    .arguments('list')
    .action(list);

const runCommmand = new Command('run')
    .description('run the filter with name, print resulting tasks')
    .option(
        '-o --output <format>',
        'output format for the tasks, available formats: table, json, csv',
        'table'
    )
    .arguments('<name>')
    .action(run);

export const FilterCommand = new Command('filter')
    .alias('f')
    .addCommand(saveCommand)
    .addCommand(updateCommand)
    .addCommand(deleteCommand)
    .addCommand(runCommmand)
    .addCommand(listCommand);
