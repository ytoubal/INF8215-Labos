import argparse
import csv


from wine_testers import RandomWineTester
from my_wine_tester import MyWineTester, MyWineTesterNN


def main():
    ###
    # (1) ouvrir params.train_file
    ###
    print("")
    print("#" * 50)
    print(f"loading {params.train_file}...")
    X_train = []
    y_train = []
    with open(params.train_file, "r") as f:
        file_reader = csv.reader(f, delimiter=';')
        for idx, row in enumerate(file_reader):
            if idx == 0:
                print(f'Column names are: [{"; ".join(row)}]')
            else:
                X_train.append(row[:-1])  # all columns except the last one
                y_train.append([int(row[0]), int(row[-1])])  # only the first and last columns
    assert len(X_train) == len(y_train)
    print(f"got {len(X_train)} training lines.\n")

    ###
    # (2) entrainer un modèle sur ce fichier
    ###
    print("-" * 50)
    print("Creating model...")
    print("-" * 50)
    # model = RandomWineTester()
    model = MyWineTester()
    print(f"{model}\n")

    print("-" * 50)
    print("Training model on training data...")
    print("-" * 50)
    model.train(X_train, y_train)
    print("done.\n")

    # compute training-set accuracy:
    print("-" * 50)
    print(f"Predicting on training data...")
    print("-" * 50)
    y_pred_train = model.predict(X_train)
    print(f"training set accuracy: {model.get_accuracy(y_pred_train, y_train)}\n")

    ###
    # (3) faire des predictions sur params.test_file
    ###
    # (3.1) ouvrir params.test_file
    print("-" * 50)
    print(f"loading {params.test_file}...")
    print("-" * 50)
    X_test = []
    with open(params.test_file, "r") as f:
        file_reader = csv.reader(f, delimiter=';')
        for idx, row in enumerate(file_reader):
            if idx == 0:
                print(f'Column names are: [{"; ".join(row)}]')
            else:
                X_test.append(row)  # all columns since test file doesn't have a target column.
    print(f"got {len(X_test)} testing lines.\n")

    # (3.2) generate predictions
    print("-" * 50)
    print(f"making predictions...")
    print("-" * 50)
    y_pred_test = model.predict(X_test)
    print(f"got {len(y_pred_test)} predictions.\n")

    ###
    # (4) sauvegarder les predictions sur params.prediction_file
    ###
    print("-" * 50)
    print(f"saving them to {params.prediction_file}...")
    print("-" * 50)
    with open(params.prediction_file, "w", newline='') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(["id", "quality"])
        for line in y_pred_test:
            csv_writer.writerow(line)
    print("done.")
    print("#" * 50)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--train_file", type=str, required=False,
        default="./data/train.csv", help="path to train csv file"
    )
    parser.add_argument(
        "--test_file", type=str, required=False,
        default="./data/test_public.csv", help="path to test csv file"
    )
    parser.add_argument(
        "--prediction_file", type=str, required=False,
        default="./data/predictions.csv", help="path to save predictions"
    )
    params = parser.parse_args()
    main()

