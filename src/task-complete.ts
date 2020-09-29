import { isAPIError, tasks } from './client';
import { Command } from 'commander';

import { getNext } from './task-next';
import { fail, unexpected } from './utils';

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
            const complete = await tasks.complete(id);
            if (isAPIError(complete)) {
                fail(complete);
            }
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
