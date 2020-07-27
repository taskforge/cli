import { isAPIError, tasks } from '@taskforge/sdk';
import { Command } from 'commander';

import { fail, unexpected } from './utils';

async function complete(ids: string[]) {
    try {
        if (ids.length === 0) {
            const task = await tasks.current();
            if (isAPIError(task)) {
                fail(task);
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
