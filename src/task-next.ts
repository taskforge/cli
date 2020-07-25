import { isAPIError, tasks } from '@taskforge/sdk';
import { Command } from 'commander';

import { printJSON } from './printing';
import { fail, unexpected } from './utils';

async function main() {
    const cli = new Command();
    cli.option('-t --title-only', 'only display the task title')
        .option('-i --id-only', 'only display the task id')
        .option('-j --json', 'display the task as JSON')
        .parse(process.argv);

    try {
        const task = await tasks.current();
        if (isAPIError(task)) {
            if (task.code === 404) {
                console.log('All done! No more unfinished tasks.');
                return;
            }

            fail(task);
            return;
        }

        if (cli.titleOnly) {
            console.log(task.title);
        } else if (cli.idOnly) {
            console.log(task.id);
        } else if (cli.json) {
            printJSON(task);
        } else {
            console.log(task.id, task.title);
        }
    } catch (e) {
        unexpected(e);
    }
}

main();
