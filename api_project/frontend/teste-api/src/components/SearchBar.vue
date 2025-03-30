<template>
  <div>
    <input type="text" v-model="searchTerm" placeholder="Digite sua busca">
    <button @click="buscarOperadoras">Buscar</button>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'SearchBar',
  emits: ['search'],
  setup(props, { emit }) {
    const searchTerm = ref('');

    const buscarOperadoras = () => {
      emit('search', searchTerm.value);
    };

    return {
      searchTerm,
      buscarOperadoras,
    };
  },
};
</script>

<style scoped>
input {
  padding: 8px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>