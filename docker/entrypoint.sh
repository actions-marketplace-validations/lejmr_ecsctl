#!/bin/sh

# Set to fail asap
set -e 

### GitHub actions --  https://docs.github.com/en/actions/reference/environment-variables
if [ "${GITHUB_ACTIONS:-false}" = "true" ]; then
    # Defines output 
    export OUTPUT_DEFINITION_PATH=$(mktemp ${INPUT_VALIDATE:-task-definition}.XXXX)".json"
fi 

if [ -z "$OUTPUT_TASK_DEFINITION_PATH" ] && [ -z "$INPUT_TASK_DEFINITION" ]; then
    # Base command
    CMD="ecs-render --td ${INPUT_TASK_DEFINITION} --val $INPUT_VALUES"

    # Insert override
    if [ -n "$INPUT_IMAGE" ]; then
        CMD="${CMD} --set image=$INPUT_IMAGE"
    fi

    # Execute the command
    sh -c "$CMD" > $OUTPUT_TASK_DEFINITION_PATH

    # Final return of path to the file
    echo "::set-output name=task-definition::$OUTPUT_TASK_DEFINITION_PATH"
else
    exec $@
fi