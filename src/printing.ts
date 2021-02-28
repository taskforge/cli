import { table } from 'table';
import { users, sources, contexts, Task, isAPIError } from './client';

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
            context.message ?? context.detail
        );
        process.exit(1);
    }

    const source = await getSource(task.source);
    if (isAPIError(source)) {
        console.log(
            'Unexpected error retrieving source:',
            source.message ?? source.detail
        );
        process.exit(1);
    }

    const owner = await getUser(task.owner);
    if (isAPIError(owner)) {
        console.log(
            'Unexpected error retrieving owner:',
            owner.message ?? owner.detail
        );
        process.exit(1);
    }

    return {
        ...task,
        owner:
            owner.full_name && owner.full_name !== ''
                ? owner.full_name
                : owner.email,
        context: context.name,
        source: source.name
    };
}

export async function printTable(list: Task[]): Promise<void> {
    const headers = [
        'id',
        'title',
        'priority',
        'created_date',
        'completed_date',
        'source',
        'context',
        'owner'
    ];
    const data: any[][] = [headers.map(humanizeKey)];

    for (const task of await Promise.all(list.map(humanize))) {
        data.push(
            headers.map((key) => {
                const value = task[key];
                if (value === undefined || value === null) {
                    return 'null';
                }
                return value;
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

export async function printTask(task: Task): Promise<void> {
    const humanized = await humanize(task);
    const data: any[][] = Object.keys(humanized).map((key) => {
        return [humanizeKey(key), humanized[key] ? humanized[key] : 'null'];
    });

    console.log(table(data));
}
