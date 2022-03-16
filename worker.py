"""
Main worker script
"""
from pipeline import Pipeline


if __name__ == '__main__':
    pipe = Pipeline()
    pipe.run_all()
