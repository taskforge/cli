import client from './client';
import { Task } from './client/tasks';
import { printJSON } from './printing';
import { loadState } from './state';
import { unexpected } from './utils';
import { Command } from 'commander';

export async function getNext(): Promise<Task | null> {
    const state = await loadState();
    const context = state.currentContext ?? undefined;
    try {
        const task = await client.tasks.next(context);
        return task;
    } catch (e) {
        if (e.toString().toLowerCase() === 'not found') {
            return null;
        }

        throw e;
    }
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
