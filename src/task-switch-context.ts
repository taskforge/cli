import { Command } from 'commander';

import { loadState, saveState } from './state';

async function switchContext(context: string, opts: Command) {
    const state = await loadState();

    if (opts.reset && state.currentContext) {
        delete state['currentContext'];
    } else if (!opts.reset) {
        state.currentContext = context;
    }

    await saveState(state);
}

export const SwitchContextCommand = new Command('switch-context')
    .alias('sc')
    .option('-r, --reset', 'reset context back to none')
    .arguments('[context]')
    .description(
        'switch the current context, changes task next to only consider the given context'
    )
    .action(switchContext);
