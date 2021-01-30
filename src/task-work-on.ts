import { isAPIError, tasks } from './client';
import { Command } from 'commander';

import { fail, unexpected, highestPriority } from './utils';

async function workOn(givenId: string) {
    try {
        const task = await tasks.get(givenId);
        if (isAPIError(task)) {
            fail(task);
            return;
        }

        task.priority = (await highestPriority()) + 1;

        const update = await tasks.update(task);
        if (isAPIError(update)) {
            fail(update);
        }
    } catch (e) {
        unexpected(e);
    }
}

export const WorkOnCommand = new Command('work-on')
    .alias('w')
    .alias('workon')
    .description('make a task the top priority')
    .arguments('<id>')
    .action(workOn);
