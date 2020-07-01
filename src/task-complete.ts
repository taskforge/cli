import { isAPIError, tasks } from '@taskforge/sdk';
import { Command } from 'commander';

import { fail } from './utils';

async function main() {
    let toComplete: string[] = [];
    const cli = new Command();
    cli.arguments('[ids...]')
        .action(function (ids) {
            toComplete = [...ids];
        })
        .parse(process.argv);

    if (toComplete.length === 0) {
        const task = await tasks.current();
        if (isAPIError(task)) {
            fail(task);
            return;
        }

        toComplete = [task.id];
    }

    for (const id of toComplete) {
        const complete = await tasks.complete(id);
        if (isAPIError(complete)) {
            fail(complete);
        }
    }
}

main();
