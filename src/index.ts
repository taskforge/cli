import { Command } from 'commander';

import { AddCommand } from './task-add';
import { CompleteCommand } from './task-complete';
import { DeferCommand } from './task-defer';
import { FilterCommand } from './task-filter';
import { ListCommand } from './task-list';
import { LoginCommand } from './task-login';
import { NextCommand } from './task-next';
import { RegisterCommand } from './task-register';
import { ShowCommand } from './task-show';
import { TodoCommand } from './task-todo';
import { WorkOnCommand } from './task-work-on';

// eslint-disable-next-line
const { version } = require('../../package.json');

const cli = new Command();
cli.version(version)
    .addCommand(AddCommand)
    .addCommand(CompleteCommand)
    .addCommand(DeferCommand)
    .addCommand(FilterCommand)
    .addCommand(ListCommand)
    .addCommand(LoginCommand)
    .addCommand(NextCommand)
    .addCommand(RegisterCommand)
    .addCommand(ShowCommand)
    .addCommand(TodoCommand)
    .addCommand(WorkOnCommand)
    .parse(process.argv);
