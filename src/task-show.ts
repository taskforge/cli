import { isAPIError, tasks, comments } from '@taskforge/sdk';
import { Command } from 'commander';

import { fail } from './utils';
import { printJSON, printTask } from './printing';

async function main() {
    let taskId: string;
    const cli = new Command();
    cli.option(
        '-o --output',
        'how to display the task, options are: table, json, or title'
    )
        .arguments('<id>')
        .action(function (id) {
            taskId = id;
        })
        .parse(process.argv);

    try {
        const task = await tasks.get(taskId!);
        if (isAPIError(task)) {
            fail(task);
            return;
        }

        let taskComments = await comments.list(task.id);
        if (isAPIError(taskComments)) {
            if (taskComments.code !== 404) {
                fail(taskComments);
                return;
            }

            taskComments = [];
        }

        if (cli.output === 'json') {
            printJSON({ ...task, comments: taskComments });
            return;
        } else if (cli.output === 'title') {
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

main();
