<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { Bars3Icon, XMarkIcon } from "@heroicons/vue/24/outline";
import { Dialog, DialogPanel } from "@headlessui/vue";
import BrandIcon from "@/assets/brand-icon.svg";
import { computed, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import PrimaryButton from "@/components/PrimaryButton.vue";

const BRAND_HOTEL_NAME = import.meta.env.VITE_BRAND_HOTEL_NAME;

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);

const mobileMenuOpen = ref(false);

const topEntries = computed(() => {
  return [
    {
      name: "Reception",
      path: "/management/reception",
      enabled:
        currentUser.value?.role === "reception" ||
        currentUser.value?.role === "admin",
    },
    {
      name: "Service",
      path: "/management/service",
      enabled:
        currentUser.value?.role === "service" ||
        currentUser.value?.role === "admin",
    },
    {
      name: "Cleaning",
      path: "/management/cleaning",
      enabled:
        currentUser.value?.role === "cleaning" ||
        currentUser.value?.role === "admin",
    },
    {
      name: "Planning",
      path: "/management/planning",
      enabled:
        currentUser.value?.role === "planning" ||
        currentUser.value?.role === "admin",
    },
    {
      name: "Admin",
      path: "/management/admin",
      enabled: currentUser.value?.role === "admin",
    },
    {
      name: "Book",
      path: "/book",
      enabled: currentUser.value !== undefined,
    },
    {
      name: "Profile",
      path: "/profile",
      enabled: currentUser.value != undefined,
    },
  ].filter((entry) => entry.enabled);
});
</script>

<template>
  <header>
    <nav
      class="container mx-auto flex flex-row items-center justify-between p-4 text-sm"
    >
      <RouterLink to="/" class="flex flex-row items-center">
        <BrandIcon class="size-[32px] pe-2" />
        <span class="font-extrabold">{{ BRAND_HOTEL_NAME }}</span>
      </RouterLink>

      <button class="block lg:hidden" @click="mobileMenuOpen = true">
        <span class="sr-only">Open menu</span>
        <Bars3Icon class="h-6 w-6" aria-hidden="true" />
      </button>

      <div class="hidden flex-row gap-x-10 lg:flex">
        <RouterLink
          v-for="entry in topEntries"
          v-bind:key="entry.path"
          :to="entry.path"
          class="font-bold"
          >{{ entry.name }}</RouterLink
        >
        <RouterLink v-if="currentUser === undefined" to="/login"
          ><PrimaryButton class="px-8 py-3">Login</PrimaryButton></RouterLink
        >
      </div>

      <Dialog
        class="lg:hidden"
        @close="mobileMenuOpen = false"
        :open="mobileMenuOpen"
      >
        <div class="fixed inset-0 z-10" />
        <DialogPanel
          class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-surface-light px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10 dark:bg-surface-dark"
        >
          <div
            class="flex items-center justify-between text-surface-light dark:text-surface-content-dark"
          >
            <RouterLink
              to="/"
              @click="mobileMenuOpen = false"
              class="-m-1.5 flex flex-row items-center p-1.5"
            >
              <BrandIcon class="size-[32px] pe-2" />
              <span class="text-sm font-bold">{{ BRAND_HOTEL_NAME }}</span>
            </RouterLink>
            <button
              type="button"
              class="-m-2.5 rounded-md p-2.5 text-gray-700"
              @click="mobileMenuOpen = false"
            >
              <span class="sr-only">Close menu</span>
              <XMarkIcon class="h-6 w-6 dark:text-white" aria-hidden="true" />
            </button>
          </div>

          <div class="flex flex-col gap-y-2 pt-5 text-lg font-semibold">
            <RouterLink
              v-for="entry in topEntries"
              v-bind:key="entry.path"
              :to="entry.path"
              @click="mobileMenuOpen = false"
              >{{ entry.name }}</RouterLink
            >
            <RouterLink
              v-if="currentUser === undefined"
              to="/login"
              @click="mobileMenuOpen = false"
              >Login</RouterLink
            >
          </div>
        </DialogPanel>
      </Dialog>
    </nav>
  </header>

  <RouterView />
</template>
