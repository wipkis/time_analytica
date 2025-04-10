from datetime import datetime, timedelta

import pandas as pd

from util import diff_minutes


class RecordManager:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.records = pd.read_csv(csv_path, index_col=False, dtype=str)

    def get_last_row(self):
        return self.records.iloc[-1] if not self.records.empty else None

    def add_row(self, fields: list[str]):
        new_date = self.handling_prev_and_get_date(fields[0])
        new_row = {
            "date": new_date,
            "time": fields[0],
            "duration": 0,
            "act": fields[1],
            **({"category_1": fields[2]} if len(fields) > 2 else {}),
            **({"category_2": fields[3]} if len(fields) > 3 else {}),
        }

        self.records = pd.concat(
            [self.records, pd.DataFrame([new_row])], ignore_index=True
        )

    def handling_prev_and_get_date(self, time: str):
        """
        시간을 입력받아 이전 행의 duration을 업데이트한다.
        이전 행의 시간과 새 시간을 보고 새 행의 날자를 얻는다.
        """
        prev = self.get_last_row()
        if prev is None:
            return datetime.today().strftime("%Y-%m-%d")

        last_idx = self.records.index[-1]
        self.records.at[last_idx, "duration"] = diff_minutes(prev["time"], time)

        if prev["time"] <= time:
            return prev["date"]
        else:
            next_day = datetime.strptime(prev["date"], "%Y-%m-%d") + timedelta(days=1)
            return next_day.strftime("%Y-%m-%d")

    def undo(self):
        if not self.records.empty:
            self.records = self.records.iloc[:-1]

    def save(self):
        self.records.to_csv(self.csv_path, index=False)

    def to_string(self):
        return self.records[::-1].reset_index(drop=True).to_csv(sep="\t", index=False)
