import path from 'path';
import { exec, ExecException } from 'child_process';

import {
    ClientOptions,
    withOptions,
    APIError,
    isAPIError,
    users,
    Task
} from '@taskforge/sdk';

function makeid(): string {
    const length = 50;
    const characters =
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let result = '';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(
            Math.floor(Math.random() * charactersLength)
        );
    }
    return result;
}

export function fail<T>(obj: APIError | T): T {
    if (isAPIError(obj)) {
        throw new Error(`${obj.code}: ${obj.message}`);
    }

    return obj as T;
}

function options(token: string): ClientOptions {
    return {
        baseUrl: process.env.TASKFORGE_HOST as string,
        headers: {
            'Content-Type': 'application/json',
            Accepts: 'application/json'
        },
        refreshToken: '',
        token
    };
}

export async function getContextName(
    token: string,
    id: string
): Promise<string> {
    const res = await withOptions.contexts.get(options(token), id);
    if (isAPIError(res)) {
        throw new Error(`Getting Context: ${res.code}: ${res.message}`);
    }

    return res.name;
}

export async function listTasks(token: string): Promise<Task[]> {
    const res = await withOptions.tasks.list(options(token));
    if (isAPIError(res)) {
        throw new Error(`Listing Tasks: ${res.code}: ${res.message}`);
    }

    return res;
}

export async function generateTask(
    token: string,
    data?: any,
    completed?: boolean
): Promise<Task> {
    const req = {
        title: `task ${makeid()}`,
        ...data
    };

    const opts = options(token);

    const res = await withOptions.tasks.create(opts, req);
    if (isAPIError(res)) {
        throw new Error(`Generating Tasks: ${res.code}: ${res.message}`);
    }

    if (completed) {
        const completion = await withOptions.tasks.complete(opts, res.id);
        if (isAPIError(completion)) {
            throw new Error(
                `Completing Task: ${completion.code}: ${completion.message}`
            );
        }

        const task = await withOptions.tasks.get(opts, res.id);
        if (isAPIError(task)) {
            throw new Error(`Retrieving Task: ${task.code}: ${task.message}`);
        }

        return task;
    }

    return res;
}

export async function generateUser(): Promise<{
    ownerId: string;
    token: string;
}> {
    const identifier = makeid();
    const email = `test-${identifier}@example.com`;
    const password = 'test';
    const user = await users.create({
        email,
        password
    });
    if (isAPIError(user)) {
        throw new Error(`${user.code}: ${user.message}`);
    }

    const pat = await users.generatePat({ email, password });
    if (isAPIError(pat)) {
        throw new Error(`${pat.code}: ${pat.message}`);
    }

    return {
        token: pat.pat,
        ownerId: user.id
    };
}

export function cwd(): string {
    return path.normalize(path.join(__dirname, '..'));
}

export function taskBin(): string {
    return path.join(cwd(), 'bin', 'task');
}

export function spawnOpts(token: string) {
    return {
        cwd: cwd(),
        maxBuffer: 200 * 1024,
        env: {
            PATH: process.env.PATH,
            TASKFORGE_HOST: process.env.TASKFORGE_HOST,
            TASKFORGE_TOKEN: token
        }
    };
}

export async function cli(
    args: string,
    token: string
): Promise<{
    stdout: string;
    stderr: string;
    code: number;
    error: ExecException | null;
}> {
    const task = taskBin();
    const cmd = `${task} ${args}`;
    return new Promise((resolve) => {
        exec(cmd, spawnOpts(token), (error, stdout, stderr) => {
            const code = error && error.code ? error.code : 0;
            if (code !== 0) {
                console.log('Command has failed with error:', error);
                console.log('============ stdout ==============');
                console.log(stdout);
                console.log('============ stderr ==============');
                console.log(stderr);
            }

            resolve({
                error,
                code,
                stdout,
                stderr
            });
        });
    });
}
