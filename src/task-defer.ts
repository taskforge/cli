import { isAPIError, tasks } from './client';
import { Command } from 'commander';

import { fail, unexpected } from './utils';

async function defer() {
    try {
        const task = await tasks.get('next');
        if (isAPIError(task)) {
            fail(task);
            return;
        }

        const update = await tasks.update({
            ...task,
            priority: task.priority - 1
        });
        if (isAPIError(update)) {
            fail(update);
        }
    } catch (e) {
        unexpected(e);
    }
}

export const DeferCommand = new Command('defer')
    .description("defer the current task by reducing it's priority")
    .action(defer);
