import pandas as pd

def export_excel(data, output_file):

    df = pd.DataFrame(data)

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Attendance",
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