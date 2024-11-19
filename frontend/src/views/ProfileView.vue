<script setup lang="ts">
import PrimaryButton from "@/components/PrimaryButton.vue";
import SurfaceCard from "@/components/SurfaceCard.vue";
import { useAuthentication } from "@/composables/auth";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/login");
  }
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <SurfaceCard class="flex flex-col">
      <span> hello {{ currentUser?.name }} </span>
      <PrimaryButton class="w-[100px]" @click="authStore.logout"
        >Log out</PrimaryButton
      ></SurfaceCard
    >
  </main>
</template>
