function makeEmoIndexMapping(emoNames) {
    var emoIndexMapping = {};

    for (j = 0; j < emoNames.length; j++) {
        emoIndexMapping[emoNames[j]] = j;
    }

    return emoIndexMapping;
}

function convertColorToString(color, isBackground) {
    var red = color["r"].toString();
    var green = color["g"].toString();
    var blue = color["b"].toString();
    var alpha = color["a"];

    if (isBackground == true) {
        alpha = 0.25 * alpha;
    }

    alpha = alpha.toString();

    var colorString = "rgba(".concat(red);
    colorString = colorString.concat(", ").concat(green).concat(", ");
    colorString = colorString.concat(blue).concat(", ").concat(alpha);

    return colorString;
}

function makeRadarPlot(context, emoNames, emoValues) {
    emoIndexMapping = makeEmoIndexMapping(emoNames);

    var emoLabels = ["Gioia", "Fiducia", "Paura", "Sorpresa",
                     "Tristezza", "Disgusto", "Rabbia", "Anticipazione"];

    var dataToPlot = [];
    for (i = 0; i < emoLabels.length; i++) {
        key = emoLabels[i];
        value = emoValues[emoIndexMapping[key]];
        dataToPlot.push(value);
    }

    var myChart = new Chart(context, {
        type: 'radar',
        data: {
            labels: emoLabels,
            datasets: [{
                label: "Intensità",
                backgroundColor: "rgba(0, 157, 255, 0.2)",
                borderColor: "rgba(0, 157, 255, 1.0)",
                pointBackgroundColor: "rgba(0, 157, 255, 1.0)",
                data: dataToPlot
            }]
        },
        options: {
            onresize: function(instance, newSize) {
                console.log(instance);
                console.log(newSize);
            },
            maintainaspectratio: true,
            legend: {
                labels: {
                    fontSize: 16
                }
            },
            scale: {
                // display: false,
                pointLabels: {
                    fontSize: 18
                }
            }
        }
    });

    return myChart;
}

function makeLinePlot(context, dataToPlot, dataName, xLabels, color) {
    var lineColor = convertColorToString(color, false);
    var fillColor = convertColorToString(color, true);

    var myChart = new Chart(context, {
        type: 'line',
        data: {
            labels: xLabels,
            datasets: [{
                label: dataName,
                data: dataToPlot,
                borderColor: lineColor,
                backgroundColor: fillColor
            }]
        },
        options: {
            scales: {
                xAxes:[{
                    display: false
                }],
                yAxes:[{
                    display: false
                }]
            }
        }
    });

    return myChart;
}
