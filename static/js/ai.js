window.onload = function () {
    fetch(`../api/user`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        mode: 'cors'
    })
        .then(response => {
            return response.text()
        })
        .then(data => {
            data = JSON.parse(data)
            document.getElementById("boasvindas").innerHTML = `Olá <b>${data.name}</b>, faça boas escolhas!`
        })
        .catch(error => console.error(error));

    document.getElementById("indicatorsButton").style.backgroundColor = "#000000"
    document.getElementById("indicatorsButton").style.color = "#FFFFFF"
}

function changeTab(tab) {
    document.getElementById("preferences").hidden = !tab
    document.getElementById("indicators").hidden = tab

    document.getElementById("indicatorsButton").style.backgroundColor = tab ? "#FD7822" : "#000000"
    document.getElementById("aiButton").style.backgroundColor = tab ? "#000000" : "#FD7822"
    document.getElementById("indicatorsButton").style.color = tab ? "#000000" : "#FFFFFF"
    document.getElementById("aiButton").style.color = tab ? "#FFFFFF" : "#000000"

}

function rangeChange() {
    let preferences = document.getElementById("preferences")
    let numbers = preferences.getElementsByTagName("output")
    let ranges = document.querySelectorAll("input[type='range']");
    for (let i = 0; i < numbers.length; i++) {
        numbers[i].innerText = ranges[i].value
    }
}

function getpref() {
    const acao = document.getElementById('acao').value;

    fetch(`../api/getpref/${acao}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        mode: 'cors'
    })
        .then(response => {
            return response.text()
        })
        .then(data => {
            data = JSON.parse(data)
            if (!data.erro) {
                data = JSON.parse(data.pref)
                for (const key in data) {
                    if (Object.hasOwnProperty.call(data, key)) {
                        document.getElementById(key).value = data[key]
                    }
                }

            }
        })
        .catch(error => console.error(error));

}

function savepref() {
    alert("Em breve")
    /*
    const acao = document.getElementById('acao').value;
    const modelo = document.getElementById('modelo').value;

    fetch('../api/savepref', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            stock: acao,
            data: JSON.stringify({
                modelo: modelo
            })
        }),
        mode: 'cors'
    })
        .then(response => {
            return response.text()
        })
        .then(data => {
        })
        .catch(error => console.error(error));
        */

}

function updateChart() {
    alert("Em breve")
    // Busca os valores selecionados pelos usuários
    //const acao = document.getElementById('acao').value;
    /*
    const modelo = document.getElementById('modelo').value;
    const datainicio = document.getElementById('datainicio').value;
    const datafim = document.getElementById('datafim').value;
    const opcaoa = document.getElementById('opcaoa').value;
    const opcaob = document.getElementById('opcaob').value;
    var radios = document.getElementsByName('opcao');
    var valorRadio = '';
    radios.forEach(function (radio) {
        if (radio.checked) {
            valorRadio = radio.value;
        }
    });

    var checkboxes = document.getElementsByName('opcao1');
    var valoresCheckbox = [];
    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            valoresCheckbox.push(checkbox.value);
        }
    });
    */
    // Exibe os valores em um alert()
    //alert(`Ação: ${acao}\nModelo de ML: ${modelo}\nData de início: ${datainicio}\nData fim: ${datafim}\nOpção A: ${opcaoa}\nOpção B: ${opcaob}\nOpção de rádio: ${valorRadio}\nOpções de caixa de seleção: ${valoresCheckbox}`);
    //chart(acao)
}

function updateChartIndicator() {
    // Busca os valores selecionados pelos usuários

    const acao = document.getElementById('stockIndicator').value;

    const indicador = document.getElementById('indicator').value;

    //const value = document.getElementById('valueIndicator').value;

    //const period = document.getElementById('periodIndicator').value;
    /*
    const datainicio = divData.getElementById('datainicio').value;
    const datafim = document.getElementById('datafim').value;
    const opcaoa = document.getElementById('opcaoa').value;
    const opcaob = document.getElementById('opcaob').value;
    var radios = document.getElementsByName('opcao');
    var valorRadio = '';
    radios.forEach(function (radio) {
        if (radio.checked) {
            valorRadio = radio.value;
        }
    });

    var checkboxes = document.getElementsByName('opcao1');
    var valoresCheckbox = [];
    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            valoresCheckbox.push(checkbox.value);
        }
    });
    */
    // Exibe os valores em um alert()
    //alert(`Ação: ${acao}\nModelo de ML: ${modelo}\nData de início: ${datainicio}\nData fim: ${datafim}\nOpção A: ${opcaoa}\nOpção B: ${opcaob}\nOpção de rádio: ${valorRadio}\nOpções de caixa de seleção: ${valoresCheckbox}`);
    chart(acao, indicator = indicador)//, periodIndicator = period, valueIndicator = value)
}



function chart(ticket, indicator, periodIndicator, valueIndicator) {
    var dataPoints1 = [], dataPoints2 = [], dataPoints3 = [], dataPointsLine = [];

    var stock = ticket
    const today = new Date();
    var dataMin = new Date(today.getFullYear(), today.getMonth(), 0)
    var dataMax = new Date(today.getFullYear(), today.getMonth() + 1, today.getDate())

    //Gráfico

    stockChart = new CanvasJS.StockChart("chartContainer", {
        exportEnabled: true,
        theme: "light3",
        title: {
            text: stock
        },
        charts: [{
            toolTip: {
                shared: true
            },
            axisX: {
                lineThickness: 5,
                tickLength: 0,
                labelFormatter: function (e) {
                    return "";
                },
                crosshair: {
                    enabled: true,
                    snapToDataPoint: true,
                    labelFormatter: function (e) {
                        return ""
                    }
                }
            },
            axisY2: {
                title: "Preço",
                prefix: "R$ "
            },
            legend: {
                verticalAlign: "top",
                horizontalAlign: "left"
            },
            data: [{
                name: "Preço (BRL)",
                yValueFormatString: "R$ #,###.##",
                axisYType: "secondary",
                type: "candlestick",
                risingColor: "green",
                fallingColor: "red",
                dataPoints: dataPoints1
            },
            {
                type: "line",
                showInLegend: true,
                name: indicator + " (Indicador)",
                axisYType: "secondary",
                yValueFormatString: "R$ #,##0.00",
                xValueFormatString: "MMMM",
                dataPoints: dataPointsLine
            }]
        }, {
            height: 100,
            toolTip: {
                shared: true
            },
            axisX: {
                crosshair: {
                    enabled: true,
                    snapToDataPoint: true
                }
            },
            axisY2: {
                prefix: "R$ ",
                title: "BRL"
            },
            legend: {
                horizontalAlign: "left"
            },
            data: [{
                yValueFormatString: "R$ #,###.##",
                axisYType: "secondary",
                name: "BRL",
                dataPoints: dataPoints2
            }]
        }],
        navigator: {
            data: [{
                color: "blue",
                dataPoints: dataPoints3
            }],
            slider: {
                minimum: dataMin,
                maximum: dataMax
            }
        }
    });

    /*
    [{
        "date": "2018-01-01",
        "open": 196.85,
        "high": 200.5,
        "low": 186.15,
        "close": 189.01,
        "volume_ltc": 15010.83,
        "volume_brl": 2889247.98
    },
    {
        ...
    },
    {
        ...
    }]
    */
//&period=${periodIndicator}&column=${valueIndicator}
    if (indicator) {
        $.getJSON(`../api/${indicator}?ticket=${ticket}`, function (json) {


            jsonData = json.data;
            let data = [];

            console.log(jsonData.indicator_name)

            for (let date in jsonData.Open) {

                const indicador = jsonData[json.indicator_name][date]

                if (indicador <= -9999)
                    continue

                const obj = {
                    date: date,
                    open: jsonData.Open[date],
                    high: jsonData.High[date],
                    low: jsonData.Low[date],
                    close: jsonData.Close[date],
                    volume: jsonData.Volume[date],
                    dividends: jsonData.Dividends[date],
                    "Stock Splits": jsonData["Stock Splits"][date],
                    indicator: indicador

                };
                data.push(obj);
            }

            for (var i = 0; i < data.length; i++) {
                dataPoints1.push({
                    x: new Date(data[i].date),
                    y: [Number(data[i].open), Number(data[i].high), Number(data[i].low), Number(data[i].close)],
                    color: data[i].open < data[i].close ? "green" : "red"
                });;
                dataPoints2.push({
                    x: new Date(data[i].date),
                    y: Number(data[i].volume),
                    color: data[i].open < data[i].close ? "green" : "red"
                });
                dataPoints3.push({
                    x: new Date(data[i].date),
                    y: Number(data[i].close)
                });
                dataPointsLine.push({
                    x: new Date(data[i].date),
                    y: Number(data[i].indicator),
                });

            }
            stockChart.render();
        });

    }
    else {
        $.getJSON(`../api/data/${ticket}`, function (data) {
            for (var i = 0; i < data.length; i++) {
                dataPoints1.push({
                    x: new Date(data[i].date),
                    y: [Number(data[i].open), Number(data[i].high), Number(data[i].low), Number(data[i].close)],
                    color: data[i].open < data[i].close ? "green" : "red"
                });;
                dataPoints2.push({
                    x: new Date(data[i].date),
                    y: Number(data[i].volume_brl),
                    color: data[i].open < data[i].close ? "green" : "red"
                });
                dataPoints3.push({
                    x: new Date(data[i].date),
                    y: Number(data[i].close)
                });
            }
            stockChart.render();
        });
    }
}