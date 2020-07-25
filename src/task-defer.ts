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

        task.priority--;

        const update = await tasks.update(task);
        if (isAPIError(update)) {
            fail(update);
        }
    } catch (e) {
        unexpected(e);
    }
}

main();
