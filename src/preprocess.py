"""
Data Preprocessing Module
"""

import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

from config import (
    TRAIN_DATA,
    TEST_DATA,
    PROCESSED_TRAIN,
    PROCESSED_TEST,
    ENCODER_PATH
)

# ------------------------------------
# Dataset Column Names
# ------------------------------------

COLUMN_NAMES = [
    "duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot",
    "num_failed_logins","logged_in","num_compromised","root_shell",
    "su_attempted","num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login",
    "is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate",
    "same_srv_rate","diff_srv_rate","srv_diff_host_rate",
    "dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate",
    "dst_host_srv_serror_rate",
    "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
    "label",
    "difficulty"
]


def preprocess_dataframe(df, encoders=None):

    df.columns = COLUMN_NAMES

    # Binary Classification
    df["label"] = df["label"].apply(
        lambda x: "normal" if x == "normal" else "attack"
    )

    categorical_columns = [
        "protocol_type",
        "service",
        "flag",
        "label"
    ]

    if encoders is None:
        encoders = {}

        for column in categorical_columns:

            encoder = LabelEncoder()

            df[column] = encoder.fit_transform(df[column])

            encoders[column] = encoder

    else:

        for column in categorical_columns:

            df[column] = encoders[column].transform(df[column])

    return df, encoders


def main():

    print("Loading Training Dataset...")

    train_df = pd.read_csv(TRAIN_DATA, header=None)

    train_df, encoders = preprocess_dataframe(train_df)

    train_df.to_csv(PROCESSED_TRAIN, index=False)

    print("Training Dataset Processed.")

    print("Loading Testing Dataset...")

    test_df = pd.read_csv(TEST_DATA, header=None)

    test_df, _ = preprocess_dataframe(
        test_df,
        encoders
    )

    test_df.to_csv(PROCESSED_TEST, index=False)

    joblib.dump(encoders, ENCODER_PATH)

    print("Testing Dataset Processed.")

    print("Encoders Saved Successfully.")

    print("Preprocessing Completed.")


if __name__ == "__main__":
    main()