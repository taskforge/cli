import { Command } from 'commander';

import { loginOrRegister } from './registration';

async function register() {
    await loginOrRegister();
}

export const RegisterCommand = new Command('register')
    .description('register a new account with the taskforge server')
    .action(register);
