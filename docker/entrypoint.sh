#!/bin/sh

# Defines output 
export OUTPUT_TASK_DEFINITION_PATH="task-definition-rendered.json"
env

# Set to fail asap
set -e pipetail

# Base command
CMD="ecs-render --td $INPUT_TASK_DEFINITION --val $INPUT_VALUES"

# Insert override
if [ -n "$INPUT_IMAGE" ]; then
    CMD="${CMD} --set image=$INPUT_IMAGE"
fi

# Execute the command
echo $CMD
sh -c "$CMD" > $OUTPUT_TASK_DEFINITION_PATH

# Final return of path to the file
echo "::set-output name=task-definition::$OUTPUT_TASK_DEFINITION_PATH"