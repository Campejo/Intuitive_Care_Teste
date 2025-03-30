<template>
  <div>
    <h2>Resultados da Busca</h2>
    <ul v-if="resultados.length > 0">
      <li v-for="(operadora, index) in resultados" :key="index">
        {{ operadora.Nome_Fantasia }} ({{ operadora.Registro_ANS }}) - CNPJ: {{ operadora.CNPJ }}
      </li>
    </ul>
    <p v-else>Nenhum resultado encontrado.</p>
  </div>
</template>

<script>
export default {
  name: 'SearchResults',
  props: {
    resultados: Array,
  },
};
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

li:last-child {
  border-bottom: none;
}
</style>