import { isAPIError, tasks } from '@taskforge/sdk';
import { Command } from 'commander';

import { fail, unexpected, highestPriority } from './utils';

async function main() {
    let givenId = 'fail';
    const cli = new Command();
    cli.arguments('<id>')
        .action(function (id) {
            givenId = id;
        })
        .parse(process.argv);

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

main();
