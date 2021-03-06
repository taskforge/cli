import client from './client';
import { emailRegex, unexpected } from './utils';
import kleur from 'kleur';
import ora from 'ora';
import prompts from 'prompts';

export async function loginOrRegister(register = true) {
    const { email, password } = await prompts([
        {
            name: 'email',
            message: 'Email:',
            type: 'text',
            validate: (value) => value.match(emailRegex)
        },
        { name: 'password', message: 'Password:', type: 'password' }
    ]);

    try {
        if (register) {
            const { fullName } = await prompts([
                {
                    name: 'fullName',
                    message: 'Full Name (optional):',
                    type: 'text'
                }
            ]);
            const registerSpinner = ora('Creating your account').start();
            await client.users.create({
                email,
                password,
                fullName
            });
            registerSpinner.stopAndPersist({
                text: kleur.bold('Registered successfully!'),
                prefixText: kleur.green('✔')
            });
        }

        const spinner = ora('Generating a personal access token').start();
        const pat = await client.users.generatePAT(email, password);
        spinner.stopAndPersist({
            text: kleur.bold('Generated token'),
            prefixText: kleur.green('✔')
        });

        console.log('Your personal access token is:');
        console.log('\n', pat.pat, '\n');
        console.log(
            'This token must be set as the environment variable' +
                ' TASKFORGE_TOKEN for use with this CLI. Add this to your shell' +
                ' configuration file to use it:'
        );
        console.log('\n', `export TASKFORGE_TOKEN='${pat.pat}'`, '\n');
        console.log(
            kleur.yellow('WARNING!'),
            'This personal access token can be revoked but it gives full permissions' +
                ' to operate on taskforge as your user. Protect it like a password.'
        );
    } catch (e) {
        unexpected(e);
        process.exit(5);
    }
}
