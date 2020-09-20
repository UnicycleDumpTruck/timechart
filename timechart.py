import csv
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

days = {
    "mon": "Monday",
    "tue": "Tuesday",
    "wed": "Wednesday",
    "thu": "Thursday",
    "fri": "Friday",
    "sat": "Saturday & Sunday",
}

exhibits = {
    "at": "Around Town",
    "htt": "Hit The Trail",
    "iw": "IdeaWorks",
    "kg": "Kid Grid",
    "mp": "Moneypalooza",
    "pz": "Putting Zoo",
    "p2p": "Power2Play",
    "rpw": "River Playway",
    "sea": "Sea Shapes",
    "sdl": "Seedlings",
    "sp": "Splash",
    "stm": "STEMOsphere",
    "sn": "Stepnotes",
    "sun": "Sun Sprouts",
    "th": "Toddlers Hollow",
}

tasks = {
    "dps": "Spray, Prop Swap",
    "wd": "Wipe Down While Open",
    "ps": "Prop Swap",
}

dates_for_days = {
    "mon": "2020-09-08",
    "tue": "2020-09-09",
    "wed": "2020-09-10",
    "thu": "2020-09-11",
    "fri": "2020-09-12",
    "sat": "2020-09-13",
    "sun": "2020-09-14",
}


def formatDate(weekday, time_of_day):
    if len(time_of_day) == 4:
        time = f"{time_of_day[0:2]}:{time_of_day[2:]}:00"
    else:
        time = f"{time_of_day[0]}:{time_of_day[1:2]}:00"
    date = f"{dates_for_days.get(str(weekday))} {time}"
    # print(date)
    return date


def formatTime(time):
    if int(time) < 1300:
        return f"{time[0:2]}:{time[2:]}"
    else:
        return f"{int(time[0:2])-12}:{time[2:]}"


with open("input.csv", "r") as input_file:
    reader = csv.DictReader(input_file)
    events = list(reader)
    for row in events:
        row["EndDate"] = formatDate(row["Day"], row["End"])
        row["exhibit1"] = exhibits.get(row["exhibit1"])
        row["exhibit2"] = exhibits.get(row["exhibit2"])
        if row["exhibit2"]:
            row["Exhibits"] = f"{row['exhibit1']} &<br>{row['exhibit2']}"
        else:
            row["Exhibits"] = row["exhibit1"]
        row["Task"] = tasks[row["Task"]]
        row[
            "Time"
        ] = f"{row['Exhibits']}<br>{row['Task']}<br>{formatTime(row['Start'])} - {formatTime(row['End'])}"
        row["StartDate"] = formatDate(row["Day"], row["Start"])

all_events_df = pd.DataFrame(events)


def plotSingleDay(ddf, day):
    print(day)
    df = ddf.loc[all_events_df["Day"] == day]
    if len(df):
        print(df)
        fig = px.timeline(
            df,
            x_start="StartDate",
            x_end="EndDate",
            y="Exhibits",
            color="Task",
            text="Time",
        )
        fig.update_yaxes(autorange="reversed")

        fig.update_layout(
            title=f"{days[day]} Exhibit Cleaning",
            xaxis_tickformat="%-I:%M",
            font_color="blue",
            font_size=10,
            title_font_family="Arial",
            title_font_color="red",
            legend_title_font_color="green",
        )
        fig.update_xaxes(tick0=0.25)
        config = {"displayModeBar": True}
        fig.show(config=config)


for day in days.keys():
    plotSingleDay(all_events_df, day)


def printExhibitTimes(df):

    for ex in exhibits.values():
        # ex_df = edf.loc[edf["exhibit2"] == ex]
        print(ex)
        single_exhibit_df = df[df.isin([ex]).any(axis=1)]

        if len(single_exhibit_df) > 0:
            print(single_exhibit_df[["Day", "Exhibits", "Start", "End", "Task"]])


carts_df = all_events_df.loc[all_events_df["Task"] != tasks["wd"]]
print(carts_df)

printExhibitTimes(carts_df)