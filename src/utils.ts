import kleur from 'kleur';
import { APIError, tasks, isAPIError } from '@taskforge/sdk';

export const emailRegex = /\S+@\S+\.\S+/;

export function fail(err: APIError): void {
    console.log(kleur.red('ERROR'), err.message);
    process.exit(err.code);
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
