let conte = document.getElementById('conte'); 
let tit = document.getElementById('tit'); 
let grafica = document.getElementById('grafica'); 
let aceptar = document.getElementById('aceptar'); 

let lista_tit = ['REGION', 'PCR','P.RAPIDA','P.ANTIGENOS','TOTAL CASOS','FALLECIDOS']  
let lista_region = []
let lista_pcr = []
let lista_prapida = [];
let lista_pantigeno = [];
let lista_totalcasos = [];
let lista_fallecidos = []; 

$.post('/', {}, function (data) {
	console.log(data); 
	llenaLista(data); 
	creaTit(); 
	creaTabla(data);
});


function creaTabla(lista) 
{
	for (let i = 0; i < 6; i++) 
	{
		let divcol = document.createElement('div');
		divcol.id = i + '-'; 
		for (let j = 0; j < 26; j++) 
		{
			let divcel = document.createElement('div'); 
			divcel.id = i + '-' + j + '-';
			divcel.innerHTML = lista[i][j]; 
			divcol.appendChild(divcel); 
		}
		conte.appendChild(divcol); 
	}	
}

function creaTit() 
{
	for (let i = 0; i < 6; i++) 
	{
		let divtit = document.createElement('div'); 
		divtit.innerHTML = lista_tit[i]; 
		divtit.onclick = function () {
			graficando(i); 
		}
		tit.appendChild(divtit);
	}	
}

function llenaLista(data)
{
	lista_region = [];
	lista_pcr = [];
	lista_prapida = [];
	lista_pantigeno = [];
	lista_totalcasos = [];
	lista_fallecidos = []; 
	for (let i = 0; i < 26; i++) 
	{
		lista_region.push(data[0][i]);
		lista_pcr.push(data[1][i]);
		lista_prapida.push(data[2][i]);
		lista_pantigeno.push(data[3][i]);
		lista_totalcasos.push(data[4][i]);
		lista_fallecidos.push(data[5][i]); 
	}
}

function graficando(n) 
{
	lista_valor = [];
	etiqueta = ''; 
	switch (n) 
	{
		case 1: 
			lista_valor = lista_pcr; etiqueta = 'pcr'; break;
		case 2: 
			lista_valor = lista_prapida; etiqueta = 'prueba rapida'; break;
		case 3: 
			lista_valor = lista_pantigeno; etiqueta = 'prueba - antigeno'; break;
		case 4: 
			lista_valor = lista_totalcasos; etiqueta = 'total de casos'; break;
		case 5: 
			lista_valor = lista_fallecidos; etiqueta = 'fallecidos'; break;
		default: return; 
	}

	var speedData = {
		labels: lista_region, 
		datasets: [{
			label: etiqueta,
			data: lista_valor
		}]
	};
	
	var chartOptions = {
		legend: {
			display: true,
			position: 'top',
			labels: {
				boxWidth: 80,
				fontColor: 'black'
			}
		}
	}; 
	
	grafica.innerHTML = '';
	grafica.innerHTML = '<canvas id="micanvas" width="650" height="450"></canvas>';

	lineChart = new Chart(micanvas, {
		type: 'line',
		data: speedData,
		options: chartOptions
	});	
}
