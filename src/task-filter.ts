import client from './client';
import { printList } from './printing';
import { unexpected } from './utils';
import { Command } from 'commander';

async function save(name: string, query: string[]): Promise<void> {
    const joined = query.join(' ');
    if (!joined || joined == '') {
        console.log('Must provide a query!');
        process.exit(1);
    }

    try {
        await client.filters.create({
            name,
            query: joined
        });
    } catch (e) {
        unexpected(e);
    }
}

async function update(name: string, query: string[]): Promise<void> {
    const joined = query.join(' ');
    if (!joined || joined == '') {
        console.log('Must provide a query!');
        process.exit(1);
    }

    try {
        const filter = await client.filters.byName(name);
        await client.filters.update({
            ...filter,
            query: joined
        });
    } catch (e) {
        unexpected(e);
    }
}

async function del(name: string): Promise<void> {
    try {
        const filter = await client.filters.byName(name);
        await client.filters.del(filter.id);
    } catch (e) {
        unexpected(e);
    }
}

async function run(name: string, opts: Command): Promise<void> {
    try {
        const filter = await client.filters.byName(name);
        const list = await client.tasks.search(filter.query);
        printList(list, opts.output);
    } catch (e) {
        unexpected(e);
    }
}

async function list(opts: Command): Promise<void> {
    try {
        const list = await client.filters.list();
        for (const f of list) {
            if (opts.verbose) {
                console.log(f.name, f.query);
            } else {
                console.log(f.name);
            }
        }
    } catch (e) {
        unexpected(e);
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
