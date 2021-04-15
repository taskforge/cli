import defaultClient, { Client } from '../src/client';
import { Filter } from '../src/client/filters';
import { isAPIError, APIError } from '../src/client/model-client';
import { Task } from '../src/client/tasks';
import { exec, ExecException } from 'child_process';
import os from 'os';
import path from 'path';

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
        throw new Error(obj.message);
    }

    return obj as T;
}

export async function getContextName(
    token: string,
    id: string
): Promise<string> {
    const client = new Client(token, process.env.TASKFORGE_HOST!);
    return (await client.contexts.get(id)).name;
}

export async function listTasks(token: string): Promise<Task[]> {
    const client = new Client(token, process.env.TASKFORGE_HOST!);
    return await client.tasks.list();
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
    const client = new Client(token, process.env.TASKFORGE_HOST!);
    const task = await client.tasks.create(req);

    if (completed) {
        await client.tasks.complete(task.id);
        return await client.tasks.get(task.id);
    }

    return task;
}

export async function generateUser(): Promise<{
    ownerId: string;
    token: string;
    email: string;
}> {
    const identifier = makeid();
    const email = `test-${identifier}@example.com`;
    const password = 'test';
    await defaultClient.users.create({
        email,
        password
    });
    const pat = await defaultClient.users.generatePAT(email, password);
    const client = new Client(pat.pat, process.env.TASKFORGE_HOST!);
    const retrievedUser = await client.users.get('me');
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
    const client = new Client(token, process.env.TASKFORGE_HOST!);
    return await client.filters.list();
}

export async function createContext(
    token: string,
    name: string
): Promise<string> {
    const client = new Client(token, process.env.TASKFORGE_HOST!);
    const res = await client.contexts.create({ name });
    return res.id;
}
