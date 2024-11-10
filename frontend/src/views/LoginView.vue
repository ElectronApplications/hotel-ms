<script setup lang="ts">
import SurfaceCard from "@/components/SurfaceCard.vue";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { onBeforeMount } from "vue";

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);

onBeforeMount(() => {
  if (currentUser.value !== undefined) {
    router.push("/profile");
  }
});
</script>

<template>
  <main class="container mx-auto flex justify-center pt-2">
    <SurfaceCard class="h-[600px] w-[500px] text-center"
      >Login form!!!</SurfaceCard
    >
  </main>
</template>
