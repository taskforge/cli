import { tasks, Task, isAPIError } from '@taskforge/sdk';
import { Table } from 'console-table-printer';
import { fail } from './utils';

export function printTable(list: Task[]): void {
    const table = new Table();
    table.addRows(list);
    table.printTable();
}

export function printJSON(list: any): void {
    console.log(list);
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

export function printTask(task: Task): void {
    const table = new Table({
        title: task.title
    });

    function prop<K extends keyof Task>(obj: Task, key: K) {
        return obj[key];
    }

    table.addRows(
        Object.keys(task)
            .filter((key) => key !== 'title')
            .map((key) => {
                return {
                    field: key,
                    value: prop(task, key as keyof Task)
                };
            })
    );

    table.printTable();
}
