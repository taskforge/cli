import { isAPIError, tasks } from '@taskforge/sdk';
import { Command } from 'commander';

import { fail, highestPriority } from './utils';

async function main() {
    let givenId: string = 'fail';
    const cli = new Command();
    cli.arguments('<id>')
        .action(function (id) {
            givenId = id;
        })
        .parse(process.argv);

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
}

main();
