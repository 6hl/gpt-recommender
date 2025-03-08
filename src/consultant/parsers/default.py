from abc import ABC, abstractmethod

import pandas as pd

from ..base_types import Ratings


class DefaultParser(ABC):

    @abstractmethod
    def parse(self):
        raise NotImplementedError


class FilterRatings:

    @staticmethod
    def collate_ratings(review_df: pd.DataFrame, n_samples: int = 10) -> Ratings:
        highest_ratings = FilterRatings.get_highest_ratings(
            review_df=review_df, n_samples=n_samples
        )
        lowest_ratings = FilterRatings.get_lowest_ratings(
            review_df=review_df[~review_df.title.isin(highest_ratings.title)],  # type: ignore
            n_samples=n_samples,
        )
        most_recent = FilterRatings.get_most_recent(
            review_df=review_df, n_samples=n_samples
        )
        return Ratings(
            highest=highest_ratings,
            lowest=lowest_ratings,
            recent=most_recent,
        )

    @staticmethod
    def get_highest_ratings(
        review_df: pd.DataFrame, n_samples: int = 10
    ) -> pd.DataFrame:
        return (
            review_df.sort_values(by="rating", ascending=False)
            .iloc[:n_samples]
            .reset_index(drop=True)
        )

    @staticmethod
    def get_lowest_ratings(
        review_df: pd.DataFrame, n_samples: int = 10
    ) -> pd.DataFrame:
        return (
            review_df.sort_values(by="rating", ascending=True)
            .iloc[:n_samples]
            .reset_index(drop=True)
        )

    @staticmethod
    def get_most_recent(review_df: pd.DataFrame, n_samples: int = 10) -> pd.DataFrame:
        if "date" not in review_df.columns:
            return review_df.iloc[:n_samples]
        return review_df.sort_values(by="date", ascending=False)
