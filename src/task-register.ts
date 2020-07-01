import { Command } from 'commander';

import { loginOrRegister } from './registration';

async function main() {
    const cli = new Command();
    cli.parse(process.argv);
    await loginOrRegister();
}

main();
