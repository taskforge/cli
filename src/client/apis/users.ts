import {
    isCredentials,
    APIError,
    Credentials,
    isUser,
    User,
    isPAT,
    PAT
} from '../types';
import { pusher, defaultPush, crud } from '../generate';
import { setDefaultCreds } from '../options';

export interface LoginArgs {
    email: string;
    password: string;
}

const loginWithOptions = pusher<LoginArgs, Credentials>(
    '/v1/tokens',
    'POST',
    isCredentials
);

const loginWithDefaults = defaultPush(loginWithOptions);

const login = async (args: LoginArgs): Promise<Credentials | APIError> => {
    const creds = await loginWithDefaults(args);
    if (isCredentials(creds)) {
        setDefaultCreds(creds);
    }

    return creds;
};

const generatePatWithOptions = pusher<LoginArgs, PAT>(
    '/v1/tokens/pat',
    'POST',
    isPAT
);

const generatePat = defaultPush(generatePatWithOptions);

export interface UserCreateArgs {
    email: string;
    password: string;
    full_name?: string;
}

const createUser = pusher<UserCreateArgs, User>('/v1/users', 'POST', isUser);

const { defaulted, optionable } = crud<UserCreateArgs, User>(
    '/v1/users',
    isUser
);

export const withOptions = {
    ...optionable,
    create: createUser,
    loginWithOptions,
    generatePatWithOptions
};

export default {
    ...defaulted,
    create: defaultPush(createUser),
    login,
    generatePat
};
