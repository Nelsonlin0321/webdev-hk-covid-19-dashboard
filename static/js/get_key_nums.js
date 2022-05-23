var g_numDataUrl = 'https://chp-dashboard.geodata.gov.hk/covid-19/data/keynum.json';
var g_autoUpdateKeyFigures = true;
var g_autoUpdateInterval = 5 * 60;

function getDeltaText(v, p) {
    var d = v - p;
    if (d < 0) return '▼ ' + (d * -1);
    if (d >= 0) return '▲ ' + (d);
}


function updateKeyNums() {
    $.ajax({
        dataType: "json",
        url: g_numDataUrl,
        cache: false
    }).done(function( data, textStatus, jqXHR ) {
        // console.log('num data', data);
        $('#confirmed').text(data.Confirmed2.toLocaleString('en'));
        $('#discharged').text(data.Discharged.toLocaleString('en'));
        $('#dischargedD').text(getDeltaText(data.Discharged, data.P_Discharged));
        $('#hospitalized').text(data.Hospitalised.toLocaleString('en'));
        $('#hospitalizedD').text(getDeltaText(data.Hospitalised, data.P_Hospitalised));
        $('#critical').text(data.Critical.toLocaleString('en'));
        $('#criticalD').text(getDeltaText(data.Critical, data.P_Critical));
        $('#death').text(data.Death.toLocaleString('en'));
        $('#deathD').text(getDeltaText(data.Death, data.P_Death));
        // $('#local').text(getDeltaText(data.LocalCasesAdded, 0));
        // $('#imported').text(getDeltaText(data.ImportedCasedAdded, 0));
        $('#local').text(getDeltaText(data.Local_Case2, 0));
        $('#imported').text(getDeltaText(data.Import_Case2, 0));
        //$('#local-rel').text(getDeltaText(data.Local_Case2_Related, 0));
        //$('#imported-rel').text(getDeltaText(data.Import_case2_Related, 0));
        $('#asymptomatic').text(data.Asymptomatic.toLocaleString('en'));
        $('#repositive').text(data.RePositive.toLocaleString('en'));
        $('#positiveCase').text(data.Confirmed.toLocaleString('en'));
        // $('#positiveCaseD').text(getDeltaText(data.Confirmed, data.P_Confirmed));
        $('#positiveCaseD').text(formatDeltaText(data.Confirmed_Delta));
    })
    .fail(function( jqXHR, textStatus, errorThrown ) {
        console.error('Error getting latest key figures.')
    });

    if(g_autoUpdateKeyFigures) {
        setTimeout(function() {
            updateKeyNums();
        }, g_autoUpdateInterval * 1000);
    }
}

$(function () {
    updateKeyNums();
})

