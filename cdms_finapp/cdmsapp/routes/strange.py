
from flask_smorest import Blueprint, abort

blp = Blueprint("strange", "strangeTable",
                description="Doctor Strange Table for Rainfall")

@blp.route("/strange/<yieldtype>/<rainfall_in_mm>")
def get_rainfall_yield(yieldtype, rainfall_in_mm):
    data = StrangeTable.strange
    rainfall_yield = 0
    rainfall = int(rainfall_in_mm)
    if rainfall > 1500:
        return '<h2>The data is out of range</h2>'
    else:
        for idx, row in enumerate(data):
            if idx == 0:
                if rainfall<=int(row['rainfall_mm']):
                    rainfall_yield=float(row['good_yield'])
            else:
                rainfall_mm_previous = int(data[idx-1]['rainfall_mm'])
                rainfall_mm = int(row['rainfall_mm'])
                if yieldtype.lower() == 'good':
                    if rainfall> int(rainfall_mm_previous) and rainfall<=int(rainfall_mm):
                        rainfall_yield = float(row['good_yield'])
                    # else:
                    #     rainfall_yield = int(rainfall_mm_previous)
                elif yieldtype.lower() == 'average':
                    if rainfall > int(rainfall_mm_previous) and rainfall<=int(rainfall):
                        rainfall_yield = float(row['average_yield'])
                else:
                    if rainfall > int(rainfall_mm_previous) and rainfall<=int(rainfall):
                        rainfall_yield = float(row['bad_yield'])
        return f'<h2>{rainfall_yield}</h2>'


class StrangeTable:
    strange = [
        {
        "rainfall_mm": "25",
        "good_runoff": "0.1",
        "good_yield": "0.25",
        "average_runoff": "0.1",
        "average_yield": "0.25",
        "bad_runoff": "0.05",
        "bad_yield": "0.13"
        },
        {
        "rainfall_mm": "50",
        "good_runoff": "0.2",
        "good_yield": "1",
        "average_runoff": "0.15",
        "average_yield": "0.75",
        "bad_runoff": "0.1",
        "bad_yield": "0.5"
        },
        {
        "rainfall_mm": "75",
        "good_runoff": "0.4",
        "good_yield": "3",
        "average_runoff": "0.3",
        "average_yield": "2.25",
        "bad_runoff": "0.2",
        "bad_yield": "1.5"
        },
        {
        "rainfall_mm": "100",
        "good_runoff": "0.7",
        "good_yield": "7",
        "average_runoff": "0.5",
        "average_yield": "5",
        "bad_runoff": "0.3",
        "bad_yield": "3"
        },
        {
        "rainfall_mm": "125",
        "good_runoff": "1",
        "good_yield": "12.5",
        "average_runoff": "0.7",
        "average_yield": "8.75",
        "bad_runoff": "0.5",
        "bad_yield": "6.25"
        },
        {
        "rainfall_mm": "150",
        "good_runoff": "1.5",
        "good_yield": "22.5",
        "average_runoff": "1.1",
        "average_yield": "16.5",
        "bad_runoff": "0.7",
        "bad_yield": "10.5"
        },
        {
        "rainfall_mm": "175",
        "good_runoff": "2.1",
        "good_yield": "36.75",
        "average_runoff": "1.5",
        "average_yield": "26.25",
        "bad_runoff": "1",
        "bad_yield": "17.5"
        },
        {
        "rainfall_mm": "200",
        "good_runoff": "2.8",
        "good_yield": "56",
        "average_runoff": "2.1",
        "average_yield": "42",
        "bad_runoff": "1.4",
        "bad_yield": "28"
        },
        {
        "rainfall_mm": "225",
        "good_runoff": "3.5",
        "good_yield": "78.75",
        "average_runoff": "2.6",
        "average_yield": "53.5",
        "bad_runoff": "1.7",
        "bad_yield": "38.25"
        },
        {
        "rainfall_mm": "250",
        "good_runoff": "4.3",
        "good_yield": "107.75",
        "average_runoff": "3.2",
        "average_yield": "80",
        "bad_runoff": "2.1",
        "bad_yield": "52.5"
        },
        {
        "rainfall_mm": "275",
        "good_runoff": "5.2",
        "good_yield": "143",
        "average_runoff": "3.9",
        "average_yield": "107.25",
        "bad_runoff": "2.6",
        "bad_yield": "71.5"
        },
        {
        "rainfall_mm": "300",
        "good_runoff": "6.2",
        "good_yield": "136",
        "average_runoff": "4.6",
        "average_yield": "138",
        "bad_runoff": "3.1",
        "bad_yield": "93"
        },
        {
        "rainfall_mm": "325",
        "good_runoff": "7.2",
        "good_yield": "234",
        "average_runoff": "5.4",
        "average_yield": "175.5",
        "bad_runoff": "3.6",
        "bad_yield": "117"
        },
        {
        "rainfall_mm": "350",
        "good_runoff": "8.3",
        "good_yield": "290",
        "average_runoff": "6.2",
        "average_yield": "217",
        "bad_runoff": "4.1",
        "bad_yield": "143.5"
        },
        {
        "rainfall_mm": "375",
        "good_runoff": "9.4",
        "good_yield": "325.5",
        "average_runoff": "7",
        "average_yield": "262.5",
        "bad_runoff": "4.7",
        "bad_yield": "176.25"
        },
        {
        "rainfall_mm": "400",
        "good_runoff": "10.5",
        "good_yield": "420",
        "average_runoff": "7.8",
        "average_yield": "312",
        "bad_runoff": "5.2",
        "bad_yield": "208"
        },
        {
        "rainfall_mm": "425",
        "good_runoff": "11.6",
        "good_yield": "493",
        "average_runoff": "8.7",
        "average_yield": "369.75",
        "bad_runoff": "5.8",
        "bad_yield": "232"
        },
        {
        "rainfall_mm": "450",
        "good_runoff": "12.8",
        "good_yield": "576",
        "average_runoff": "9.6",
        "average_yield": "432",
        "bad_runoff": "6.4",
        "bad_yield": "288"
        },
        {
        "rainfall_mm": "475",
        "good_runoff": "13.9",
        "good_yield": "660.25",
        "average_runoff": "10.4",
        "average_yield": "494",
        "bad_runoff": "6.9",
        "bad_yield": "327.75"
        },
        {
        "rainfall_mm": "500",
        "good_runoff": "16",
        "good_yield": "800",
        "average_runoff": "11.25",
        "average_yield": "562.5",
        "bad_runoff": "7.5",
        "bad_yield": "377"
        },
        {
        "rainfall_mm": "525",
        "good_runoff": "16.1",
        "good_yield": "845.25",
        "average_runoff": "12",
        "average_yield": "630",
        "bad_runoff": "8",
        "bad_yield": "420"
        },
        {
        "rainfall_mm": "550",
        "good_runoff": "17.3",
        "good_yield": "951.5",
        "average_runoff": "12.9",
        "average_yield": "709.5",
        "bad_runoff": "8.6",
        "bad_yield": "473"
        },
        {
        "rainfall_mm": "575",
        "good_runoff": "18.4",
        "good_yield": "1058",
        "average_runoff": "13.8",
        "average_yield": "793.5",
        "bad_runoff": "9.2",
        "bad_yield": "529"
        },
        {
        "rainfall_mm": "600",
        "good_runoff": "19.5",
        "good_yield": "1170",
        "average_runoff": "14.6",
        "average_yield": "878",
        "bad_runoff": "9.7",
        "bad_yield": "582"
        },
        {
        "rainfall_mm": "625",
        "good_runoff": "20.6",
        "good_yield": "1287.5",
        "average_runoff": "15.4",
        "average_yield": "962.5",
        "bad_runoff": "10.3",
        "bad_yield": "643.75"
        },
        {
        "rainfall_mm": "650",
        "good_runoff": "21.8",
        "good_yield": "1417",
        "average_runoff": "16.3",
        "average_yield": "1059.5",
        "bad_runoff": "10.9",
        "bad_yield": "708.5"
        },
        {
        "rainfall_mm": "675",
        "good_runoff": "22.9",
        "good_yield": "1545.75",
        "average_runoff": "17.1",
        "average_yield": "1154.25",
        "bad_runoff": "11.4",
        "bad_yield": "769.5"
        },
        {
        "rainfall_mm": "700",
        "good_runoff": "24",
        "good_yield": "1618",
        "average_runoff": "18",
        "average_yield": "1260",
        "bad_runoff": "12",
        "bad_yield": "840"
        },
        {
        "rainfall_mm": "725",
        "good_runoff": "25.1",
        "good_yield": "1819.75",
        "average_runoff": "18.8",
        "average_yield": "1363",
        "bad_runoff": "12.5",
        "bad_yield": "906.25"
        },
        {
        "rainfall_mm": "750",
        "good_runoff": "26.3",
        "good_yield": "1972.5",
        "average_runoff": "19.7",
        "average_yield": "1477.5",
        "bad_runoff": "13.1",
        "bad_yield": "982.5"
        },
        {
        "rainfall_mm": "775",
        "good_runoff": "27.4",
        "good_yield": "2123.5",
        "average_runoff": "20.5",
        "average_yield": "1580",
        "bad_runoff": "13.7",
        "bad_yield": "1061.75"
        },
        {
        "rainfall_mm": "800",
        "good_runoff": "28.5",
        "good_yield": "2218.5",
        "average_runoff": "21.3",
        "average_yield": "1704",
        "bad_runoff": "14.2",
        "bad_yield": "1136"
        },
        {
        "rainfall_mm": "825",
        "good_runoff": "29.6",
        "good_yield": "2442",
        "average_runoff": "22.2",
        "average_yield": "1831.5",
        "bad_runoff": "14.8",
        "bad_yield": "1221"
        },
        {
        "rainfall_mm": "850",
        "good_runoff": "30.8",
        "good_yield": "2618",
        "average_runoff": "23.1",
        "average_yield": "1963.5",
        "bad_runoff": "15.4",
        "bad_yield": "1309"
        },
        {
        "rainfall_mm": "875",
        "good_runoff": "31.9",
        "good_yield": "2791.25",
        "average_runoff": "23.9",
        "average_yield": "2090.25",
        "bad_runoff": "15.9",
        "bad_yield": "1391"
        },
        {
        "rainfall_mm": "900",
        "good_runoff": "33",
        "good_yield": "2917",
        "average_runoff": "24.7",
        "average_yield": "2223",
        "bad_runoff": "16.7",
        "bad_yield": "1485"
        },
        {
        "rainfall_mm": "925",
        "good_runoff": "34.1",
        "good_yield": "3154.25",
        "average_runoff": "25.5",
        "average_yield": "2358.75",
        "bad_runoff": "17",
        "bad_yield": "1572"
        },
        {
        "rainfall_mm": "975",
        "good_runoff": "36.4",
        "good_yield": "3549",
        "average_runoff": "27.3",
        "average_yield": "2661.75",
        "bad_runoff": "18.2",
        "bad_yield": "1774"
        },
        {
        "rainfall_mm": "1000",
        "good_runoff": "37.5",
        "good_yield": "3750",
        "average_runoff": "28.1",
        "average_yield": "2810",
        "bad_runoff": "18.7",
        "bad_yield": "1870"
        },
        {
        "rainfall_mm": "1125",
        "good_runoff": "43.1",
        "good_yield": "4348",
        "average_runoff": "32.3",
        "average_yield": "3633.75",
        "bad_runoff": "21.5",
        "bad_yield": "2418"
        },
        {
        "rainfall_mm": "1250",
        "good_runoff": "48",
        "good_yield": "6100",
        "average_runoff": "36.6",
        "average_yield": "4575",
        "bad_runoff": "24.4",
        "bad_yield": "3050"
        },
        {
        "rainfall_mm": "1375",
        "good_runoff": "54.4",
        "good_yield": "7480",
        "average_runoff": "40.8",
        "average_yield": "5610",
        "bad_runoff": "27.7",
        "bad_yield": "3740"
        },
        {
        "rainfall_mm": "1500",
        "good_runoff": "60",
        "good_yield": "9000",
        "average_runoff": "45",
        "average_yield": "6750",
        "bad_runoff": "30",
        "bad_yield": "4500"
        }
    ]