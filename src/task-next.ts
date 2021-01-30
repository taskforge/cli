import { isAPIError, Task, tasks } from './client';
import { Command } from 'commander';

import { printJSON } from './printing';
import { fail, unexpected } from './utils';
import { loadState } from './state';

export async function getNext(): Promise<Task | null> {
    const state = await loadState();
    const requestOptions = state.currentContext
        ? { context: state.currentContext }
        : {};

    const task = await tasks.current(requestOptions);
    if (isAPIError(task)) {
        if (task.code !== 404) fail(task);
        return null;
    }

    return task;
}

async function next(opts: Command) {
    try {
        const task = await getNext();
        if (!task) {
            console.log('All done! No more unfinished tasks.');
            return;
        }

        if (opts.titleOnly) {
            console.log(task.title);
        } else if (opts.idOnly) {
            console.log(task.id);
        } else if (opts.json) {
            printJSON(task);
        } else {
            console.log(task.id, task.title);
        }
    } catch (e) {
        unexpected(e);
    }
}

export const NextCommand = new Command('next')
    .alias('n')
    .alias('current')
    .description('show your next or "current" task')
    .option('-t --title-only', 'only display the task title')
    .option('-i --id-only', 'only display the task id')
    .option('-j --json', 'display the task as JSON')
    .action(next);
