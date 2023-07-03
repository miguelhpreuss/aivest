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

    changeModelSelected("lr")
}

function changeModelSelected(m) {

    if (m == "lr") {
        document.getElementById("model_exp").innerText = "Com modelo de Linear Regression está sendo realizado um processo que envolve dados de ações de uma determinada empresa. Primeiro, é obtido um conjunto de dados históricos das ações. Em seguida, são definidas algumas características (features) que serão usadas posteriormente no processo de treinamento de um modelo. Essas características incluem informações como preço de fechamento (Close), preço de abertura (Open), médias móveis exponenciais (EMA) de diferentes períodos e médias móveis simples (SMA) de diferentes períodos, além do RSI (Relative Strength Index). Os dados históricos são processados para calcular as médias móveis exponenciais (EMA) e as médias móveis simples (SMA) com os períodos pré-definidos. Também é calculado o RSI. Essas informações são adicionadas ao conjunto de dados existente. Em seguida, são realizadas algumas transformações nos dados para prepará-los para o treinamento do modelo. A coluna 'Close' é deslocada para cima (shift) em uma posição para se tornar a coluna alvo 'y1'. O conjunto de dados é então limitado às características selecionadas ('features') e à coluna alvo 'y1'. Os dados para treinamento são separados do último dado disponível para previsão. Os valores faltantes são removidos dos dados de treinamento. Em seguida, um modelo de regressão linear é criado e treinado usando as características ('features') e a coluna alvo ('y1') dos dados de treinamento. Os dados para previsão são selecionados e são feitas as previsões usando o modelo treinado. As previsões são convertidas em uma lista. Os dados para previsão são convertidos em um formato adequado para serem exportados como um objeto JSON. Finalmente, o resultado é retornado como um objeto JSON contendo os dados para previsão e a previsão de um (1) dia."
    }
    else if (m = "lstm") {
        document.getElementById("model_exp").innerText = "Com o modelo de Long Short-Term Memory está sendo feito um processo que envolve previsão de valores de ações usando um modelo treinado. Primeiro, apenas ações de bancos da B3 estão na lista de modelos treinados previamente. Em seguida, é definido um tamanho de janela igual a 60. Os dados históricos das ações são obtidos, com o período de 3 meses e intervalo de 1 dia. A coluna 'Close' dos dados é selecionada. Em seguida, são selecionados os últimos 60 registros dos dados. Esse objeto é um escalador usado para normalizar os dados. Os dados são redimensionados e preparados para serem usados como entrada para o modelo de previsão. Um modelo é carregado a partir de um arquivo. Os dados transformados são usados para fazer previsões usando o modelo carregado. As previsões são desnormalizadas e convertidas de volta para a escala original. Em seguida, as previsões são convertidas em uma lista. Os índices dos dados originais são convertidos para strings. Os dados originais e as previsões são convertidos para um objeto JSON. Finalmente, o resultado é retornado em um JSON com os dados das ações e 5 dias de previsão."
        alert("Em Breve")
    }
/*
    fetch(`../api/availableOptions?model=${m}`, {
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
            lista = JSON.parse(data)
            const select = document.getElementById('acao');

            lista.forEach(item => {
                const option = document.createElement('option');
                option.value = item;
                option.text = item;
                select.appendChild(option);
            });
        })
        .catch(error => console.error(error));
        */
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


}

function updateChart() {

    const acao = document.getElementById('acao').value;

    const modelo = document.getElementById('modelo').value;

    chart(acao, "SMA", modelo)
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
    chart(acao, indicador, undefined)//, periodIndicator = period, valueIndicator = value)
}



function chart(ticket, indicator, model, periodIndicator, valueIndicator) {
    var dataPoints1 = [], dataPoints2 = [], dataPoints3 = [], dataPointsLine = [];

    var stock = ticket
    const today = new Date();
    var dataMin = new Date(today.getFullYear(), today.getMonth()-1, 0)
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
                name: model ? model + " (Modelo)":indicator + " (Indicador)",
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
    if (true) {
        $.getJSON(`../api/${indicator}?ticket=${ticket}`, function (json) {

            jsonData = json.data;
            let data = [];

            for (let date in jsonData.Open) {

                if (date == "2023-06-30 00:00:00-03:00")
                    continue

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



            if (model) {
                $.getJSON(`../api/predict_${model}?stock=${stock}`, function (json2) {

                    for (let i = 0; i < (model == "lstm" ? 5 : 1); i++) {
                        const currentDate = new Date();
                        currentDate.setDate(currentDate.getDate() + i);
                        const formattedDate = currentDate.toISOString().split("T")[0] + " 00:00:00-03:00";
                        let obj = {}

                        obj.date = formattedDate,
                        obj.indicator = json2.predictions[0][i]

                        data.push(obj);
                    }
                    console.log(data)

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
            else{
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
            }


        });

    }
}