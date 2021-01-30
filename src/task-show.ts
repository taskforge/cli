import { Comment, isAPIError, tasks, comments } from './client';
import { Command } from 'commander';

import { fail } from './utils';
import { printJSON, printTask } from './printing';

async function show(id: string, opts: Command) {
    try {
        const task = await tasks.get(id);
        if (isAPIError(task)) {
            fail(task);
            return;
        }

        let taskComments: Comment[] = [];
        const commentRes = await comments.list(task.id);
        if (isAPIError(commentRes)) {
            if (commentRes.code !== 404) {
                fail(commentRes);
                return;
            }
        } else {
            taskComments = commentRes.data;
        }

        if (opts.output === 'json') {
            printJSON({ ...task, comments: taskComments });
            return;
        } else if (opts.output === 'title') {
            console.log(task.title);
        } else {
            printTask(task);
        }

        if (taskComments.length > 0) {
            console.log(
                '------------------------------------COMMENTS------------------------------------'
            );
        }

        for (const comment of taskComments) {
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
