import pandas as pd

from datetime import datetime

def calculate_summary(df):

    summary = []

    for emp_id, emp_df in df.groupby("employee_id"):

        name = emp_df.iloc[0]["employee_name"]

        working_days = 0
        absent_days = 0

        late_count = 0
        total_late_minutes = 0

        early_leave_count = 0
        total_early_leave_minutes = 0

        for _, row in emp_df.iterrows():

            check_in = row["check_in"]
            check_out = row["check_out"]

            if pd.notna(check_in) and str(check_in).strip():

                working_days += 1

                try:

                    in_time = datetime.strptime(
                        check_in,
                        "%H:%M"
                    )

                    standard_in = datetime.strptime(
                        "08:39",
                        "%H:%M"
                    )

                    if in_time > standard_in:

                        late_minutes = int(
                            (in_time - standard_in)
                            .seconds / 60
                        )

                        late_count += 1
                        total_late_minutes += late_minutes

                except:
                    pass

            else:

                absent_days += 1

            if pd.notna(check_out) and str(check_out).strip():

                try:

                    out_time = datetime.strptime(
                        check_out,
                        "%H:%M"
                    )

                    standard_out = datetime.strptime(
                        "17:30",
                        "%H:%M"
                    )

                    if out_time < standard_out:

                        early_leave_minutes = int(
                            (standard_out - out_time)
                            .seconds / 60
                        )

                        early_leave_count += 1

                        total_early_leave_minutes += (
                            early_leave_minutes
                        )

                except:
                    pass

        summary.append({

            "employee_id": emp_id,

            "employee_name": name,

            "working_days": working_days,

            "absent_days": absent_days,

            "late_count": late_count,

            "late_minutes": total_late_minutes,

            "early_leave_count": early_leave_count,

            "early_leave_minutes":
                total_early_leave_minutes
        })

    return pd.DataFrame(summary)


def export_excel(data, output_file):

    df = pd.DataFrame(data)
    summary_df = calculate_summary(df)

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Attendance",
            index=False
        )

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )


        for emp in df["employee_name"].unique():

            emp_df = df[
                df["employee_name"] == emp
            ]

            sheet_name = emp[:31]

            emp_df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False
            )

    return output_file