<script setup lang="ts">
import { RouterLink } from "vue-router";
import SurfaceCard from "@/components/SurfaceCard.vue";
import DefaultProfileImage from "@/assets/default-profile.png";
import { useAuthentication } from "@/composables/auth";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import SecondaryButton from "@/components/SecondaryButton.vue";
import ExpandableImage from "@/components/ExpandableImage.vue";

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
    <SurfaceCard class="flex flex-col items-center lg:flex-row lg:items-start">
      <ExpandableImage
        class="w-[250px]"
        imgClass="rounded-full"
        :src="currentUser?.picture ?? DefaultProfileImage"
        :alt="currentUser?.name"
      />
      <div class="flex flex-col ps-8 pt-4">
        <h1 class="text-4xl font-extrabold">
          {{ currentUser?.name }}
        </h1>
        <h2 class="pt-2 text-xl font-semibold">
          {{ currentUser?.phone_number }}
        </h2>
        <span class="pt-2" v-if="currentUser?.role !== 'client'">
          {{ currentUser?.role }}
        </span>
      </div>
      <div class="flex flex-row justify-end pt-8 lg:grow lg:pt-0">
        <div class="flex flex-col gap-2">
          <SecondaryButton class="w-[250px]" @click="authStore.logout"
            >Log out</SecondaryButton
          >
          <RouterLink to="/change-password">
            <SecondaryButton class="w-[250px]">Change password</SecondaryButton>
          </RouterLink>
        </div>
      </div>
    </SurfaceCard>
  </main>
</template>
