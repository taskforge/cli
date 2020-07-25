import { isAPIError, tasks } from '@taskforge/sdk';
import { Command } from 'commander';

import { fail, unexpected } from './utils';

async function main() {
    const cli = new Command();
    cli.parse(process.argv);

    try {
        const task = await tasks.get('next');
        if (isAPIError(task)) {
            fail(task);
            return;
        }

        const taskList = await tasks.search('completed = false');
        if (isAPIError(taskList)) {
            fail(taskList);
            return;
        }
        const lowestPriority = Math.min(...taskList.map((t) => t.priority));

        const update = await tasks.update({
            ...task,
            priority:
                task.priority === lowestPriority
                    ? lowestPriority - 1
                    : lowestPriority
        });
        if (isAPIError(update)) {
            fail(update);
        }
    } catch (e) {
        unexpected(e);
    }
}

main();
