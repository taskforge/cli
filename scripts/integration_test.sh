#!/bin/bash

export TASKFORGE_CONFIG_DIR=$(mktemp -d)
export CONFIG_FILE=$TASKFORGE_CONFIG_DIR/config.toml
export TASKFORGE_TEST_DB=$(mktemp)
rm -f $TASKFORGE_TEST_DB

function setup() {
    killall taskforged || true
    echo "[list]
name = 'sqlite'

[list.config]
file_name = '$TASKFORGE_TEST_DB'

[server]
port = 60095" > $CONFIG_FILE
    info "Using config: $CONFIG_FILE"
    cat $CONFIG_FILE
}

function cleanup() {
    killall taskforged
    rm -rf $TASKFORGE_CONFIG_DIR
    rm -f $TASKFORGE_TEST_DB
}

function log() {
    echo $(date) $@
}

function fail() {
    log "[FAIL]" $@
    log "current task list:"
    task list
    cleanup
    exit 1
}

function info() {
    log "[INFO]" $@
}

function x() {
    CMD="$@"
    info Running $CMD
    $CMD
    if [[ $? != 0 ]]; then
        fail "Failed to run $CMD"
    fi
}

function check_for_output() {
    CMD="$@"
    info Running $CMD
    OUTPUT=$($CMD)
    if [[ -z $OUTPUT ]]; then
        fail "Command '$@' recieved no output"
    fi    
}


setup

x task add complete the Taskforge tutorial
check_for_output task list
check_for_output task next
x task add another default priority task
x task add --priority 2 a high priority task

if [[ $(x task next | grep "a high priority task") == "" ]]; then
    fail "task next did not show the high priority task"
fi

x task done

info "Running task next"
OUT=$(task next)
if [[ $(echo $OUT | grep "a high priority task") != "" ]]; then
    fail "task high priority task was not completed"
fi

check_for_output task query completed = false
check_for_output task todo

x task workon $(task query --output text 'title = "another default priority task"' | sed 's/Task(//g' | sed 's/)//g')

info "Running task next"
OUT=$(task next)
if [[ $(echo $OUT | grep "another default priority task") == "" ]]; then
    fail "task next did not show the another default priority task"
fi

x task done

info "Running task next"
OUT=$(task next)
if [[ $(echo $OUT | grep "another default priority task") != "" ]]; then
    fail "task another default priority task was not completed"
fi

cleanup
info "Integration tests passed!"
