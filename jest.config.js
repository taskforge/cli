module.exports = {
    transform: { '^.+\\.(t|j)sx?$': 'ts-jest' },
    testRegex: '.*(jsx?|tsx?)$',
    modulePaths: ['<rootDir>/src'],
    moduleDirectories: ['node_modules', 'src'],
    testPathIgnorePatterns: ['/node_modules/', 'utils\\.ts'],
    moduleNameMapper: {
        '@backend/(.*)': '<rootDir>/src/$1',
        '@tests/(.*)': '<rootDir>/tests/$1'
    },
    roots: ['tests'],
    moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node']
};
