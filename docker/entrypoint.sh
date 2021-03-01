#!/bin/sh

# Set to fail asap
set -e pipetail

### GitHub actions --  https://docs.github.com/en/actions/reference/environment-variables
if [ "${GITHUB_ACTIONS:-false}" = "true" ]; then
    # Defines output 
    export OUTPUT_DEFINITION_PATH=$(mktemp ${INPUT_VALIDATE:-task-definition}.XXXX)".json"

    # Base command
    CMD="ecs-render --td ${INPUT_DEFINITION} --val $INPUT_VALUES"

    # Insert override
    if [ -n "$INPUT_IMAGE" ]; then
        CMD="${CMD} --set image=$INPUT_IMAGE"
    fi

    # Execute the command
    sh -c "$CMD" > $OUTPUT_DEFINITION_PATH

    # Final return of path to the file
    echo "::set-output name=definition::$OUTPUT_DEFINITION_PATH"

    # Finish
    exit 0
fi

### TODO: GitLab

# For any other platform just a passthrough (Jenkins)
exec $@