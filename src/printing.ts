import { table } from 'table';
import {
    users,
    sources,
    contexts,
    tasks,
    Task,
    isAPIError
} from '@taskforge/sdk';
import { fail } from './utils';

function idMemo<T>(fn: (id: string) => Promise<T>): (id: string) => Promise<T> {
    const memo: { [id: string]: T } = {};
    return async (id: string): Promise<T> => {
        if (memo[id]) {
            return memo[id];
        }

        const model = await fn(id);
        return model;
    };
}

const getContext = idMemo(contexts.get);
const getSource = idMemo(sources.get);
const getUser = idMemo(users.get);

function humanizeKey(key: string): string {
    if (key == 'id') {
        return 'ID';
    }

    const words = key.match(/[A-Za-z][a-z]*/g) || [];
    return words
        .map((word) => {
            return word.charAt(0).toUpperCase() + word.substring(1);
        })
        .join(' ');
}

async function humanize(task: Task): Promise<any> {
    const context = await getContext(task.context);
    if (isAPIError(context)) {
        console.log(
            'Unexpected error retrieving context:',
            context.code,
            context.message
        );
        process.exit(1);
    }

    const source = await getSource(task.source);
    if (isAPIError(source)) {
        console.log(
            'Unexpected error retrieving source:',
            source.code,
            source.message
        );
        process.exit(1);
    }

    const owner = await getUser(task.owner);
    if (isAPIError(owner)) {
        console.log(
            'Unexpected error retrieving owner:',
            owner.code,
            owner.message
        );
        process.exit(1);
    }

    return {
        ...task,
        owner: owner.fullName !== '' ? owner.fullName : owner.email,
        context: context.name,
        source: source.name
    };
}

export async function printTable(list: Task[]): Promise<void> {
    const headers = Object.keys(list[0]);
    const data: any[][] = [headers.map(humanizeKey)];

    for (const task of await Promise.all(list.map(humanize))) {
        data.push(
            headers.map((key) => {
                return task[key] ? task[key] : 'null';
            })
        );
    }

    const options = {
        drawHorizontalLine: (index: number, size: number) => {
            return index === 0 || index === 1 || index === size;
        }
    };

    console.log(table(data, options));
}

export function printJSON(obj: any): void {
    console.log(JSON.stringify(obj, null, 2));
}

export function printList(list: Task[], format: string): void {
    switch (format) {
        case 'json':
            printJSON(list);
            break;
        default:
            if (list.length === 0) {
                console.log('No tasks to show!');
                return;
            }

            printTable(list);
    }
}

export async function highestPriority(): Promise<number> {
    const current = await tasks.current();
    if (isAPIError(current)) {
        if (current.code === 404) {
            return 2;
        }

        fail(current);
        return 0;
    }

    return current.priority;
}

export async function printTask(task: Task): Promise<void> {
    const humanized = await humanize(task);
    const data: any[][] = Object.keys(humanized).map((key) => {
        return [humanizeKey(key), humanized[key] ? humanized[key] : 'null'];
    });

    console.log(table(data));
}
