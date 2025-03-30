<template>
  <div id="app">
    <h1>Buscar Operadoras</h1>
    <SearchBar @search="handleSearch" />
    <SearchResults :resultados="searchResults" />
  </div>
</template>

<script>
import { ref } from 'vue';
import SearchBar from './components/SearchBar.vue';
import SearchResults from './components/SearchResults.vue';

export default {
  name: 'App',
  components: {
    SearchBar,
    SearchResults,
  },
  setup() {
    const searchResults = ref([]);

    const handleSearch = async (searchTerm) => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/buscar_operadoras?termo=${searchTerm}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Dados recebidos do servidor:', data);
        searchResults.value = data;
      } catch (error) {
        console.error('Erro ao buscar operadoras:', error);
        searchResults.value = []; // Limpa os resultados em caso de erro
      }
    };

    return {
      searchResults,
      handleSearch,
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>