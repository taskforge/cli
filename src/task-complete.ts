import client from './client';
import { getNext } from './task-next';
import { unexpected } from './utils';
import { Command } from 'commander';

async function complete(ids: string[]) {
    try {
        if (ids.length === 0) {
            const task = await getNext();
            if (!task) {
                console.log(
                    'No ids given and no next task found. Nothing to do.'
                );
                return;
            }

            ids = [task.id];
        }

        for (const id of ids) {
            await client.tasks.complete(id);
        }
    } catch (e) {
        unexpected(e);
    }
}

export const CompleteCommand = new Command('complete')
    .alias('done')
    .alias('c')
    .description('complete tasks')
    .arguments('[ids...]')
    .action(complete);
