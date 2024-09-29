import joblib
import pandas as pd
import numpy as np

from model.Recommended.config import cfg


def convert_float_to_int(df):
    """type conversion from float to int"""
    float_cols = df.select_dtypes(include=["float"]).columns

    for col in float_cols:
        df[col] = df[col].astype(int)

    return df


def preprocess_places_list(places_list_str):
    """
    Preprocesses the places list string into a list of places.

    Parameters:
    places_list_str (str): String representation of the places list.

    Returns:
    list: A list of places.
    """
    places_list = places_list_str.replace("[", "").replace("]", "").replace("'", "").replace(", ", ",")
    return list(map(str, places_list.split(",")))


def generate_final_df(info, new_user_info, places_list):
    """
    Generates the final DataFrame based on user information and places list.

    Parameters:
    info (DataFrame): DataFrame containing area information.
    new_user_info (DataFrame): DataFrame containing new user information.
    places_list (list): List of places.

    Returns:
    DataFrame: The final DataFrame containing combined user and area information.
    """
    final_df = pd.DataFrame(columns=cfg.final_columns)

    for place in places_list:
        sido, gungu = map(str, place.split("+"))
        info_df = info[(info["SIDO"] == sido) & (info["GUNGU"] == gungu)].drop(["SIDO"], axis=1).reset_index(drop=True)
        user_data = new_user_info.drop(["sido_gungu_list"], axis=1).values.tolist()[0]
        user_data = [sido] + user_data
        user_df = pd.DataFrame([user_data] * len(info_df), columns=cfg.user_columns)
        df = pd.concat([user_df, info_df], axis=1)[cfg.features]
        df["VISIT_AREA_TYPE_CD"] = df["VISIT_AREA_TYPE_CD"].astype("string")
        final_df = pd.concat([final_df, df], axis=0)

    final_df.reset_index(drop=True, inplace=True)
    final_df.drop_duplicates(["VISIT_AREA_NM"], inplace=True)
    return final_df


def recommend_places(model, final_df):
    """
    Recommends places based on the model's predictions.

    Parameters:
    model: The predictive model.
    final_df (DataFrame): The final DataFrame containing combined user and area information.

    Returns:
    list: List of recommended places.
    """
    final_df = convert_float_to_int(final_df)
    y_pred = model.predict(final_df)
    y_pred_df = pd.DataFrame(y_pred, columns=["y_pred"])
    sorted_df = pd.concat([final_df, y_pred_df], axis=1).sort_values(by="y_pred", ascending=False).iloc[:10]
    return list(sorted_df["VISIT_AREA_NM"])


def generate_user_info_df(final_df):
    """
    Generates a DataFrame containing user information.

    Parameters:
    final_df (DataFrame): The final DataFrame containing combined user and area information.

    Returns:
    DataFrame: DataFrame containing user information.
    """
    return final_df[cfg.user_columns]


def find_hotplace(df, top_k=10):
    import random

    hotplace = df["VISIT_AREA_NM"].value_counts().reset_index()
    results = hotplace["index"][:30].tolist()
    recommended_places = random.sample(results, top_k)
    return recommended_places


def prediction(info, new_user_info, model):
    """
    Main function to generate recommendations and user information.

    Parameters:
    info (DataFrame): DataFrame containing area information.
    new_user_info (DataFrame): DataFrame containing new user information.
    model: The predictive model.

    Returns:
    list: A list containing user information and recommended places.
    """
    result = []
    places_list_str = new_user_info["sido_gungu_list"].values[0]
    places_list = preprocess_places_list(places_list_str)
    final_df = generate_final_df(info, new_user_info, places_list)

    visiting_candidates = recommend_places(model, final_df)
    user_info_df = generate_user_info_df(final_df)

    # Exception handling for empty user_info_df(해당 지역에 관광지가 없는 경우)
    if len(user_info_df) == 0:
        places = pd.read_csv(cfg.followup_places_path)
        result = find_hotplace(places)
    else:
        try:
            rec = user_info_df.iloc[0].to_list()
            rec.append(visiting_candidates)
            result.append(rec)
            result = result[0][-1]
        except:
            places = pd.read_csv(cfg.followup_places_path)
            result = find_hotplace(places)

    return result


if __name__ == "__main__":
    info = pd.read_csv(cfg.information_path)
    recommend_model = joblib.load(cfg.model_path)
    # places = pd.read_csv(cfg.places_path)
    test_data = pd.read_pickle(r"C:\workspace\K-Swipe-Backend\app\model\TestData.pkl")
    result = prediction(info, test_data, recommend_model)
