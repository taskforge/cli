import kleur from 'kleur';
import { APIError, tasks, isAPIError } from '@taskforge/sdk';

export const emailRegex = /\S+@\S+\.\S+/;

export function fail(err: APIError): void {
    console.log(kleur.red('error:'), err.message);
    process.exit(err.code);
}

export function unexpected(err: Error): void {
    console.log(kleur.red('Unexpected error:'), err.toString());
    process.exit(1);
}

export async function highestPriority(): Promise<number> {
    try {
        const current = await tasks.current();
        if (isAPIError(current)) {
            if (current.code === 404) {
                return 2;
            }

            fail(current);
            return 0;
        }

        return current.priority;
    } catch (e) {
        unexpected(e);
        return 0;
    }
}
