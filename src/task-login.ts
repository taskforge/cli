import { Command } from 'commander';
import { loginOrRegister } from './registration';

async function login() {
    await loginOrRegister(false);
}

export const LoginCommand = new Command('login')
    .description('generate a personal access token')
    .action(login);
