import client from './client';
import { printJSON, printTask } from './printing';
import { Command } from 'commander';

async function show(id: string, opts: Command) {
    try {
        const task = await client.tasks.get(id);
        const comments = await client.comments.list(0, task.id);
        if (opts.output === 'json') {
            printJSON({ ...task, comments });
            return;
        } else if (opts.output === 'title') {
            console.log(task.title);
        } else {
            printTask(task);
        }

        if (comments.length > 0) {
            console.log(
                '------------------------------------COMMENTS------------------------------------'
            );
        }

        for (const comment of comments) {
            console.log('---', comment.createdDate, '---');
            console.log(comment.body);
        }
    } catch (e) {
        console.log('Unexpected error:', e);
        process.exit(5);
    }
}

export const ShowCommand = new Command('show')
    .alias('s')
    .description('show detailed information about a task')
    .option(
        '-o --output <format>',
        'how to display the task, options are: table, json, or title'
    )
    .arguments('<id>')
    .action(show);
