import argparse
from ecs_render import render


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Render ECS Task definition from template and input variables')