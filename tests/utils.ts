import path from 'path';
import os from 'os';
import { exec, ExecException } from 'child_process';

import {
    ClientOptions,
    withOptions,
    APIError,
    isAPIError,
    users,
    Filter,
    Task
} from '../src/client';

export function makeid(): string {
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

export function genDir(): string {
    return path.join(os.tmpdir(), makeid());
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

    return res.data;
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
    email: string;
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

    const retrievedUser = await withOptions.users.get(options(pat.pat), 'me');
    if (isAPIError(retrievedUser)) {
        throw new Error(`${retrievedUser.code}: ${retrievedUser.message}`);
    }

    return {
        email,
        token: pat.pat,
        ownerId: retrievedUser.id
    };
}

export function cwd(): string {
    return path.normalize(path.join(__dirname, '..'));
}

export function taskBin(): string {
    return path.join(cwd(), 'bin', 'task');
}

export interface SpawnOpts {
    dataDir?: string;
    configDir?: string;
}

export function spawnOpts(token: string, opts?: SpawnOpts) {
    return {
        cwd: cwd(),
        maxBuffer: 200 * 1024,
        env: {
            XDG_DATA_HOME:
                opts && opts.dataDir
                    ? opts.dataDir
                    : path.join(os.tmpdir(), makeid()),
            XDG_CONFIG_HOME:
                opts && opts.configDir
                    ? opts.configDir
                    : path.join(os.tmpdir(), makeid()),
            PATH: process.env.PATH,
            TASKFORGE_HOST: process.env.TASKFORGE_HOST,
            TASKFORGE_TOKEN: token
        }
    };
}

export async function cli(
    args: string,
    token: string,
    opts?: SpawnOpts
): Promise<{
    stdout: string;
    stderr: string;
    code: number;
    error: ExecException | null;
}> {
    const task = taskBin();
    const cmd = `${task} ${args}`;
    return new Promise((resolve) => {
        exec(cmd, spawnOpts(token, opts), (error, stdout, stderr) => {
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

export async function listFilters(token: string): Promise<Filter[]> {
    const res = await withOptions.filters.list(options(token));
    if (isAPIError(res)) {
        throw new Error(`Listing Filters: ${res.code}: ${res.message}`);
    }

    return res.data;
}

export async function createContext(
    token: string,
    name: string
): Promise<string> {
    const res = await withOptions.contexts.create(options(token), { name });
    if (isAPIError(res)) {
        throw new Error(`Getting Context: ${res.code}: ${res.message}`);
    }

    return res.id;
}
