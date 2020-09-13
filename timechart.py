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
    print(date)
    return date


with open("input.csv", "r") as input_file:
    reader = csv.DictReader(input_file)
    events = list(reader)
    for row in events:
        row["Task"] = tasks[row["Task"]]
        row["Time"] = f"{row['Task']}<br>{row['Start']} - {row['End']}"
        row["Start"] = formatDate(row["Day"], row["Start"])
        row["End"] = formatDate(row["Day"], row["End"])
        row["exhibit1"] = exhibits.get(row["exhibit1"])
        row["exhibit2"] = exhibits.get(row["exhibit2"])
        if row["exhibit2"]:
            row["Exhibits"] = f"{row['exhibit1']} &<br>{row['exhibit2']}"
        else:
            row["Exhibits"] = row["exhibit1"]

print(events)

edf = pd.DataFrame(events)


def plotSingleDay(ddf, day):
    print(day)
    df = ddf.loc[edf["Day"] == day]
    if len(df):
        print(df)
        fig = px.timeline(
            df,
            x_start="Start",
            x_end="End",
            y="Exhibits",
            color="Task",
            text="Time",
        )
        fig.update_yaxes(autorange="reversed")

        fig.update_layout(
            title=f"{days[day]} Exhibit Cleaning",
            xaxis_tickformat="%H:%M",
            font_color="blue",
            font_size=10,
            title_font_family="Times New Roman",
            title_font_color="red",
            legend_title_font_color="green",
        )
        fig.update_xaxes(tick0=0.25)
        config = {"displayModeBar": True}
        fig.show(config=config)


for day in days.keys():
    plotSingleDay(edf, day)
