const selectElement = document.querySelector('#consultas')
const filtro1 = document.querySelector('#filtro1')
const filtro2 = document.querySelector('#filtro2')

selectElement.addEventListener('change', function () {
  const opcaoSelecionada = selectElement.value;
  if (opcaoSelecionada == 'consulta2') {
    filtro1.style.display = "block"
    filtro2.style.display = "block"
    filtro1.placeholder = "Digite a data (YYYY-MM-DD)"
    filtro2.placeholder = "Digite a sigla do país"
  } else if ((opcaoSelecionada == 'consulta1') || (opcaoSelecionada == 'consulta10') || (opcaoSelecionada == 'consulta11')) {
    filtro1.style.display = "block"
    filtro1.placeholder = "Digite o nome do canal"
  } else if (opcaoSelecionada == 'consulta5') {
    filtro1.style.display = "block"
    filtro1.placeholder = "Digite o nome da categoria"
  } else {
    filtro1.style.display = 'none'
    filtro2.style.display = 'none'
  }
  console.log(`Você selecionou: ${opcaoSelecionada}`);
});