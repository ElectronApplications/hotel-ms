<script setup lang="ts">
import axios from "axios";
import { onBeforeMount, ref } from "vue";

type Client = {
  id: number;
  name: string;
  phone_number: string;
};

let clients = ref<Client[]>([]);

async function fetchClients() {
  clients.value = (await axios.get("/api/client/")).data;
}

onBeforeMount(async () => {
  await fetchClients();
});
</script>

<template>
  <main class="container mx-auto">
    <div class="flex flex-col gap-y-2">
      <span v-for="c in clients" v-bind:key="c.id">
        {{ c.name }} с номером {{ c.phone_number }}
      </span>
    </div>
  </main>
</template>
