import argparse
import random
import sys

import scipy.stats

import cloudpickle
import json
import os

import numpy as np
import pandas as pd

from experiments.keras.models.housing_mlp import HousingMLP
from experiments.utils.environment_generator import EnvGen
from projectmetis.python.driver.driver_session import DriverSession
from projectmetis.python.models.model_dataset import ModelDatasetRegression

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

if __name__ == "__main__":

    script_cwd = os.path.dirname(__file__)
    print("Script current working directory: ", script_cwd, flush=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--communication_protocol", default="SYNCHRONOUS", type=str)
    parser.add_argument("--federation_rounds", default=10, type=int)
    parser.add_argument("--learners_num", default=10, type=int)
    parser.add_argument("--train_samples_per_learner", default=10, type=int)
    parser.add_argument("--test_samples", default=10, type=int)
    parser.add_argument("--nn_params_per_layer", default=10, type=int)
    parser.add_argument("--nn_hidden_layers_num", default=0, type=int)
    parser.add_argument("--data_type", default="float32", type=str)

    args = parser.parse_args()
    print(args, flush=True)

    """ Generate federated environment. """
    federation_environment = EnvGen().generate_localhost(
        federation_rounds=args.federation_rounds,
        learners_num=args.learners_num,
        gpu_devices=[-1])

    """ Load training and test data. """
    required_training_samples = int(args.learners_num * args.train_samples_per_learner)
    total_required_samples = required_training_samples + int(args.test_samples)
    housing_np = pd.read_csv(script_cwd + "/datasets/housing/original/data.csv").to_numpy()
    housing_np = housing_np[~np.isnan(housing_np).any(axis=1)]

    total_rows = len(housing_np)
    if total_required_samples > total_rows:
        diff = total_required_samples - total_rows
        for i in range(diff):
            # Append random row from the original set of rows.
            housing_np = np.vstack(
                [housing_np,
                 housing_np[random.randrange(total_rows)]])

    np.random.shuffle(housing_np)
    train_data, test_data = housing_np[:required_training_samples], housing_np[-args.test_samples:]
    # First n-1 are input features, last feature is prediction/output feature.
    x_train, y_train = train_data[:, :-1], train_data[:, -1:]
    x_test, y_test = test_data[:, :-1], test_data[:, -1:]

    x_chunks, y_chunks = np.split(x_train, args.learners_num), np.split(y_train, args.learners_num)
    datasets_path = "datasets/housing/"
    np.savez(os.path.join(script_cwd, datasets_path, "test.npz"), x=x_test, y=y_test)
    for cidx, (x_chunk, y_chunk) in enumerate(zip(x_chunks, y_chunks)):
        np.savez(os.path.join(script_cwd, datasets_path, "train_{}.npz".format(cidx)), x=x_chunk, y=y_chunk)
    for lidx, learner in enumerate(federation_environment.learners.learners):
        learner.dataset_configs.test_dataset_path = \
            os.path.join(script_cwd, datasets_path, "test.npz")
        learner.dataset_configs.train_dataset_path = \
            os.path.join(script_cwd, datasets_path, "train_{}.npz".format(lidx))

    nn_engine = "keras"
    metis_filepath_prefix = "/tmp/metis/model/"
    if not os.path.exists(metis_filepath_prefix):
        os.makedirs(metis_filepath_prefix)

    model_filepath = "{}/model_definition".format(metis_filepath_prefix)
    train_dataset_recipe_fp_pkl = "{}/model_train_dataset_ops.pkl".format(metis_filepath_prefix)
    validation_dataset_recipe_fp_pkl = "{}/model_validation_dataset_ops.pkl".format(metis_filepath_prefix)
    test_dataset_recipe_fp_pkl = "{}/model_test_dataset_ops.pkl".format(metis_filepath_prefix)

    nn_model = HousingMLP(
        params_per_layer=args.nn_params_per_layer,
        hidden_layers_num=args.nn_hidden_layers_num,
        data_type=args.data_type).get_model()
    nn_model.evaluate(x=np.random.random(x_train[0:1].shape), y=np.random.random(y_train[0:1].shape), verbose=False)
    nn_model.save(model_filepath)
    nn_model.summary()

    def dataset_recipe_fn(dataset_fp):
        dataset = np.load(dataset_fp)
        features, prices = dataset['x'], dataset['y']
        features = np.vstack(features)
        prices = np.concatenate(prices)
        mode_values, mode_counts = scipy.stats.mode(prices)
        if np.all((mode_counts == 1)):
            mode_val = np.max(prices)
        else:
            mode_val = mode_values[0]
        model_dataset = ModelDatasetRegression(
            x=features, y=prices, size=len(prices),
            min_val=np.min(prices), max_val=np.max(prices),
            mean_val=np.mean(prices), median_val=np.median(prices),
            mode_val=mode_val, stddev_val=np.std(prices))
        return model_dataset

    cloudpickle.dump(obj=dataset_recipe_fn, file=open(train_dataset_recipe_fp_pkl, "wb+"))
    cloudpickle.dump(obj=dataset_recipe_fn, file=open(test_dataset_recipe_fp_pkl, "wb+"))
    cloudpickle.dump(obj=dataset_recipe_fn, file=open(validation_dataset_recipe_fp_pkl, "wb+"))

    driver_session = DriverSession(federation_environment, nn_engine,
                                   model_definition_dir=model_filepath,
                                   train_dataset_recipe_fp=train_dataset_recipe_fp_pkl,
                                   validation_dataset_recipe_fp=validation_dataset_recipe_fp_pkl,
                                   test_dataset_recipe_fp=test_dataset_recipe_fp_pkl)
    driver_session.initialize_federation(model_weights=nn_model.get_weights())
    driver_session.monitor_federation()
    driver_session.shutdown_federation()
    statistics = driver_session.get_federation_statistics()

    with open(os.path.join(script_cwd, "experiment.json"), "w+") as fout:
        print("Execution File Output Path:", fout.name, flush=True)
        json.dump(statistics, fout, indent=4)
