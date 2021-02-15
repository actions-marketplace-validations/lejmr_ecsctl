# Amazon AWS - ECS Task renderer using Jinja2

[![Known Vulnerabilities](https://snyk.io/test/github/lejmr/amazon-ecs-render-task-definition/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/lejmr/amazon-ecs-render-task-definition?targetFile=requirements.txt)
![Code coverage](https://github.com/lejmr/amazon-ecs-render-task-definition/workflows/Code%20coverage/badge.svg)
![Unit tests](https://github.com/lejmr/amazon-ecs-render-task-definition/workflows/Unit%20tests/badge.svg)

The goal of this project is to deliver an minimalistic templating library for managing Amazon AWS ECS Task definition easily. This library is inspired by [Helm](https://helm.sh/). Therefore, it allows to split definition in multiple files and implements smart merging. The template can be written in using JSON or Yaml notation. No matter markup language is selected, all are merged together. Look at [examples](https://github.com/lejmr/test-ecs-render/)

The plan is to have the same library for deployments using GitHub, Jenkins, and Gitlab.


Example directory structure

```
.
├── complex-task-definition
│   ├── app.yaml
│   ├── db.yaml
│   └── task_properties.yaml
├── simple-task-definition.json
└── values
    ├── DEV.json
    └── PROD
        ├── environment.yaml
        └── extra.yml
```

This is how template can be constructed from two directories containing particular json/yaml files
```
  - name: Example of simple template
    uses: lejmr/amazon-ecs-render-task-definition@v1
    with:
      task-definition: complex-task-definition
      values: values/PROD
```

