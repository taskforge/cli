import client from './client';
import { unexpected, highestPriority } from './utils';
import { Command } from 'commander';

async function workOn(givenId: string) {
    try {
        const task = await client.tasks.get(givenId);
        task.priority = (await highestPriority()) + 1;
        await client.tasks.update(task);
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
