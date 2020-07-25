import { Command } from 'commander';

// eslint-disable-next-line
const { version } = require('../../package.json');

const cli = new Command();

cli.command('add', 'add a task to your list')
    .command('list', 'list and search your tasks')
    .alias('search')
    .alias('query')
    .alias('l')
    .alias('ls')
    .alias('q')
    .command('complete', 'complete tasks')
    .alias('done')
    .alias('c')
    .command(
        'show',
        'show detailed information about a task, including comments'
    )
    .alias('s')
    .command('work-on', 'make a task the top priority')
    .alias('w')
    .alias('workon')
    .command('next', 'show your next or "current" task')
    .alias('n')
    .alias('current')
    .command('todo', 'list your incomplete tasks')
    .alias('td')
    .command('register', 'register a new account with the taskforge server')
    .command('login', 'generate a personal access token')
    .version(version)
    .parse(process.argv);
