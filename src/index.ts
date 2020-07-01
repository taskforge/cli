import { Command } from 'commander';

// eslint-disable-next-line
const { version } = require('../package.json');

const cli = new Command();

process.env.TASKFORGE_HOST = 'http://localhost:8000/api';

cli.command('add', 'add a task to your list')
    .command('list', 'list your tasks')
    .command('query', 'search your tasks')
    .command('complete', 'complete tasks')
    .command('workon', 'make a task the top priority')
    .command('next', 'show your next or "current" task')
    .command('todo', 'list your incomplete tasks')
    .command('register', 'register a new account with the taskforge server')
    .command('login', 'generate a personal access token')
    .version(version)
    .parse(process.argv);
